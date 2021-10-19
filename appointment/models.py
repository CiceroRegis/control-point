import logging
import quopri
import random
import textwrap
import threading
import uuid
from datetime import timedelta
from email.mime.text import MIMEText

from django.core.mail import EmailMultiAlternatives, send_mail
from django.db import models
from django.utils import timezone
from django.utils.timezone import localtime
from django.utils.translation import gettext_lazy as _

from collaborator.models import Profile
from patient.models import Patient

logger = logging.getLogger('django')


class NotificationPatient(models.Model):
    NOTIFICATION_MODEL_ACTION = (
        ('appointment-saved', _('Notify to pacientes appointments')),
    )

    class Meta:
        db_table = 'NotificationSupportTeam'
        verbose_name = _('Notification Support Team')
        verbose_name_plural = _('Notification Support Team')

    action = models.CharField(max_length=200, choices=NOTIFICATION_MODEL_ACTION, verbose_name=_('Action'))
    patient = models.ForeignKey(Patient, on_delete=models.DO_NOTHING, verbose_name=_('Patient'))

    def __str__(self):
        return self.patient.name
    # def get_type_pacient(self):
    #     return "; ".join([p.name for p in self.patient.all()])


class TypeAppointment(models.Model):
    class Meta:
        db_table = "typeAppointment"
        verbose_name = _("typeAppointment")
        verbose_name_plural = _("typeAppointment")

    name = models.CharField(max_length=200, verbose_name=_('Name'))
    skip = models.BooleanField(default=False, verbose_name=_('Skip'))
    price = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Price of appointment'))
    updateAt = models.DateTimeField(null=False, blank=False, editable=False, auto_now=True)
    createAt = models.DateTimeField(null=False, blank=False, editable=False, auto_now_add=True)

    def __str__(self):
        return self.name


class Appointment(models.Model):
    class Meta:
        db_table = "appointment"
        verbose_name = _("appointment")
        verbose_name_plural = _("appointment")

    description = models.CharField(max_length=60, null=True, default=None, verbose_name=_('Appointment name'))
    type_appointment = models.ManyToManyField(TypeAppointment,
                                              verbose_name=_('Type appointment'))
    patient = models.ForeignKey(Patient, on_delete=models.PROTECT, verbose_name=_('Patient'))
    professional = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, verbose_name=_('Professional'))
    date_appointment = models.DateTimeField(verbose_name=_('date of appointment'))
    consulting = models.BooleanField(default=False, verbose_name=_('Consulting'))
    isCanceled = models.BooleanField(default=False, editable=False)
    calendarUUID = models.UUIDField(default=uuid.uuid4, editable=False)
    calendarOwnerTID = models.IntegerField(default=random.randrange(-214748364, 2147483647), editable=False)
    updateAt = models.DateTimeField(null=False, blank=False, editable=False, auto_now=True)
    createAt = models.DateTimeField(null=False, blank=False, editable=False, auto_now_add=True)

    @property
    def date_now(self):
        now = timezone.now()
        return now < self.date_appointment
    # def get_type_appointment(self):
    #     return "\n".join([p.name for p in self.type_appointment.all()])

    def type_appointment_list(self):
        return ', '.join([str(i) for i in self.type_appointment.all()])

    def save(self, *args, **kwargs):
        super(Appointment, self).save(*args, **kwargs)
        if self.patient.email and self.createAt:
            self.start = threading.Thread(target=self.__send_invite_ics(), args=()).start()

    def __send_invite_ics(self):
        if not self.patient.email:
            logger.warning('Patient email is empty')
            return

        try:
            email_message = '\n'.join([
                'Você possui um consulta marcada com a Mirabolante Dente',
                '{0}: {1}'.format('Consulta', self.description),
                '{0}: {1}'.format('Endereço',
                                  '<Mirabolante Dente>, CNA 01 Lote 09/10 Ed. Santos Dumond Salas 501 e 502, '
                                  'Taguatinga Norte, Brasília - DF, 72110-015'),
                '{0}: {1}'.format('Responsável pela Consulta', self.professional),
                '{0}: {1}'.format('Email do responsavel', 'www.mirabolantedente.net.com.br'),
                '{0}: {1}'.format('Seu Atendimento será dia',
                                  localtime(self.date_appointment).strftime('%d/%m/%Y %H:%M')),
            ])
            email = EmailMultiAlternatives(
                '{0} - {1}'.format(self.description, 'cancelado' if self.isCanceled else 'marcado'),
                email_message, 'Mirabolante Dente <www.mirabolantedente.net.com.br>',
                to=[self.patient.email],
            )

            # Form more information read https://tools.ietf.org/html/rfc5545
            vcalendar = [
                'BEGIN:VCALENDAR',
                'PRODID:-//Mirabolante Dente//controlpoint.app//EN',
                'VERSION:2.0',
                'CALSCALE:GREGORIAN',
                'METHOD:{0}'.format('CANCEL' if self.isCanceled else 'REQUEST'),
                'BEGIN:VEVENT',
                'DTSTART:{0}'.format(localtime(self.date_appointment + timedelta(hours=3)).strftime('%Y%m%dT%H%M%SZ')),
                'DTSTAMP:{0}'.format(localtime(self.createAt + timedelta(hours=3)).strftime('%Y%m%dT%H%M%SZ')),
                'LAST-MODIFIED:{0}'.format(localtime(self.updateAt + timedelta(hours=3)).strftime('%Y%m%dT%H%M%SZ')),
                'ORGANIZER;CN={0}:MAILTO:{1}'.format('Mirabolante Dente', 'cicerooliveira091@gmail.com'),
                'UID:{0}@control-point.app'.format(self.calendarUUID.hex.lower()),
                *['ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP='
                  'TRUE;CN={0};X-NUM-GUESTS=0:mailto:{0}'.format(g) for g in self.patient.email],
                'X-MICROSOFT-CDO-OWNERAPPTID:{0}'.format(self.calendarOwnerTID),
                'SEQUENCE:{0}'.format('1' if self.isCanceled else '0'),
                'STATUS:{0}'.format('CANCELLED' if self.isCanceled else 'CONFIRMED'),
                'SUMMARY:{0}'.format(self.description),
                'TRANSP:OPAQUE',
                'END:VEVENT',
                'END:VCALENDAR',
            ]
            text_wrap = textwrap.TextWrapper(width=75)
            text_calendar = '\n'.join(['\n '.join(text_wrap.wrap(text=i)) for i in vcalendar])

            # first create MIMEBase, then set content-transfer-encoding, then set payload
            # don't forget add in content-type header the flag method=REQUEST
            calendar = MIMEText('text', 'calendar')
            calendar.set_payload(quopri.encodestring(bytes(text_calendar.encode('utf8'))), charset='utf-8')
            calendar.replace_header('Content-Transfer-Encoding', 'quoted-printable')
            calendar.replace_header('Content-Type', 'text/calendar; charset="utf-8"; method={0}'
                                    .format('CANCEL' if self.isCanceled else 'REQUEST'))

            email.attach(calendar)
            email.attach('invite.ics', text_calendar, 'application/ics')

            email.send(fail_silently=False)
            logger.info('Email sent')
        except Exception as e:
            logger.error("Send email error", exc_info=e)

    def __notify_patient_action_saved(self):
        query_set_patient = Appointment.objects.values(
            'patient__email')
        patients = [e.get('patient__email')
                    for e in query_set_patient if e.get('patient__email', False)]
        if len(patients) < 1:
            return

        email_message = '\n'.join([
            'Você possui um consulta marcada com a Mirabolante Dente',
            '{0}: {1}'.format('Consulta', self.description),
            '{0}: {1}'.format('Endereço',
                              '<Mirabolante Dente>, CNA 01 Lote 09/10 Ed. Santos Dumond Salas 501 e 502, '
                              'Taguatinga Norte, Brasília - DF, 72110-015'),
            '{0}: {1}'.format('Responsável pela Consulta', self.professional),
            '{0}: {1}'.format('Email do responsavel', 'www.mirabolantedente.net.com.br'),
            '{0}: {1}'.format('Seu Atendimento será dia', localtime(self.date_appointment).strftime('%d/%m/%Y %H:%M')),
        ])

        if self.createAt:
            try:
                send_mail(
                    '{0}'.format(self.patient.name),
                    email_message,
                    'Mirabolante Dente <www.mirabolantedente.net.com.br>',
                    patients
                )
                logger.info('Notify patients success')
            except Exception as e:
                logger.error('Notify patients error', exc_info=e)
