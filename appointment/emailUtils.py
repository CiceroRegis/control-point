# import logging
# import quopri
# import textwrap
# import threading
# from datetime import timedelta
# from email.mime.text import MIMEText
#
# from django.core.mail import EmailMultiAlternatives, send_mail
# from django.utils.timezone import localtime
#
# from appointment.models import Appointment
#
# logger = logging.getLogger('django')
#
#
# class SendEmail(Appointment):
#
#     def save(self, *args, **kwargs):
#         super(Appointment, self).save(*args, **kwargs)
#         if self.patient.email:
#             self.start = threading.Thread(target=self.__send_invite_ics, args=()).start()
#
#         if self.isCanceled:
#             threading.Thread(target=self.__notify_patient_action_saved(), args=()).start()
#
#     def __send_invite_ics(self):
#         if not self.patient.email:
#             logger.warning('Patient email is empty')
#             return
#
#         try:
#             email_message = '\n'.join([
#                 'Você possui um consulta Confirmada com a Mirabolante Dente',
#                 '{0}: {1}'.format('Consulta', self.description),
#                 '{0}: {1}'.format('Endereço',
#                                   '<Mirabolante Dente>, CNA 01 Lote 09/10 Ed. Santos Dumond Salas 501 e 502, '
#                                   'Taguatinga Norte, Brasília - DF, 72110-015'),
#                 '{0}: {1}'.format('Responsável pela Consulta', self.professional),
#                 '{0}: {1}'.format('Email do responsavel', 'www.mirabolantedente.net.com.br'),
#                 '{0}: {1}'.format('Seu Atendimento será dia',
#                                   localtime(self.date_appointment).strftime('%d/%m/%Y %H:%M')),
#             ])
#             email = EmailMultiAlternatives(
#                 '{0} - {1}'.format(self.description, 'cancelado' if not self.date_now else 'marcado'),
#                 email_message, 'Mirabolante Dente <www.mirabolantedente.net.com.br>',
#                 to=[self.patient.email],
#             )
#
#             # Form more information read https://tools.ietf.org/html/rfc5545
#             vcalendar = [
#                 'BEGIN:VCALENDAR',
#                 'PRODID:-//Mirabolante Dente//controlpoint.app//EN',
#                 'VERSION:2.0',
#                 'CALSCALE:GREGORIAN',
#                 'METHOD:{0}'.format('CANCEL' if self.isCanceled else 'REQUEST'),
#                 'BEGIN:VEVENT',
#                 'DTSTART:{0}'.format(
#                     localtime(self.date_appointment + timedelta(hours=3)).strftime('%Y%m%dT%H%M%SZ')),
#                 'DTSTAMP:{0}'.format(localtime(self.createAt + timedelta(hours=3)).strftime('%Y%m%dT%H%M%SZ')),
#                 'LAST-MODIFIED:{0}'.format(
#                     localtime(self.updateAt + timedelta(hours=3)).strftime('%Y%m%dT%H%M%SZ')),
#                 'ORGANIZER;CN={0}:MAILTO:{1}'.format('Mirabolante Dente', 'cicerooliveira091@gmail.com'),
#                 'UID:{0}@control-point.app'.format(self.calendarUUID.hex.lower()),
#                 *['ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP='
#                   'TRUE;CN={0};X-NUM-GUESTS=0:mailto:{0}'.format(g) for g in self.patient.email],
#                 'X-MICROSOFT-CDO-OWNERAPPTID:{0}'.format(self.calendarOwnerTID),
#                 'SEQUENCE:{0}'.format('1' if self.isCanceled else '0'),
#                 'STATUS:{0}'.format('CANCELLED' if self.isCanceled else 'CONFIRMED'),
#                 'SUMMARY:{0}'.format(self.description),
#                 'TRANSP:OPAQUE',
#                 'END:VEVENT',
#                 'END:VCALENDAR',
#             ]
#             text_wrap = textwrap.TextWrapper(width=75)
#             text_calendar = '\n'.join(['\n '.join(text_wrap.wrap(text=i)) for i in vcalendar])
#
#             # first create MIMEBase, then set content-transfer-encoding, then set payload
#             # don't forget add in content-type header the flag method=REQUEST
#             calendar = MIMEText('text', 'calendar')
#             calendar.set_payload(quopri.encodestring(bytes(text_calendar.encode('utf8'))), charset='utf-8')
#             calendar.replace_header('Content-Transfer-Encoding', 'quoted-printable')
#             calendar.replace_header('Content-Type', 'text/calendar; charset="utf-8"; method={0}'
#                                     .format('CANCEL' if self.isCanceled else 'REQUEST'))
#
#             email.attach(calendar)
#             email.attach('invite.ics', text_calendar, 'application/ics')
#
#             email.send(fail_silently=False)
#             logger.info('Email sent')
#         except Exception as e:
#             logger.error("Send email error", exc_info=e)
#
#     def __notify_patient_action_saved(self):
#         query_set_patient = Appointment.objects.values(
#             'pacient__email').filter(action='appointment-saved')
#         patients = [e.get('pacient__email')
#                     for e in query_set_patient if e.get('pacient__email', False)]
#         if len(patients) < 1:
#             return
#
#         email_message = '\n'.join([
#             'Você possui um consulta Confirmada com a Mirabolante Dente',
#             '{0}: {1}'.format('Consulta', self.description),
#             '{0}: {1}'.format('Endereço',
#                               '<Mirabolante Dente>, CNA 01 Lote 09/10 Ed. Santos Dumond Salas 501 e 502, '
#                               'Taguatinga Norte, Brasília - DF, 72110-015'),
#             '{0}: {1}'.format('Responsável pela Consulta', self.professional),
#             '{0}: {1}'.format('Email do responsavel', 'www.mirabolantedente.net.com.br'),
#             '{0}: {1}'.format('Seu Atendimento será dia',
#                               localtime(self.date_appointment).strftime('%d/%m/%Y %H:%M')),
#         ])
#
#         if not self.isCanceled:
#             try:
#                 send_mail(
#                     '{0}'.format(self.patient.name),
#                     email_message,
#                     'Mirabolante Dente <www.mirabolantedente.net.com.br>',
#                     patients
#                 )
#                 logger.info('Notify pacients success')
#             except Exception as e:
#                 logger.error('Notify pacients error', exc_info=e)
