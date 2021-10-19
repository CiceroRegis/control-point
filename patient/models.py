import random

from django.db import models
from django.utils.translation import gettext_lazy as _


# Create your models here.
class Patient(models.Model):
    class Meta:
        db_table = "patient"
        verbose_name = _("patient")
        verbose_name_plural = _("patient")

    SEXO_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    name = models.CharField(max_length=100, null=True, blank=True, verbose_name=_('Name'))
    medical_record_number = models.IntegerField(default=random.randint(1, 25052020), null=True, blank=True,
                                                editable=False, verbose_name=_('Medical record number'))
    photo = models.ImageField(upload_to='photos', max_length=200, null=True, blank=True)
    rg_document = models.CharField(max_length=14, null=True, blank=True, verbose_name=_('rg document'))
    cpf_document = models.CharField(max_length=14, null=True, blank=True, verbose_name=_('cpf document'))
    date_of_birth = models.DateField(max_length=14, null=True, blank=True, verbose_name=_('Date of birth'))
    phone_number = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('phone number'))
    landline = models.CharField(max_length=15, blank=True, null=True, verbose_name=_('landline'))
    email = models.EmailField(max_length=254, blank=True, null=True)
    address = models.CharField(max_length=254, blank=True, null=True, verbose_name=_('Address'))
    sexo = models.CharField(max_length=1, blank=True, null=True, choices=SEXO_CHOICES)
    updateAt = models.DateTimeField(null=False, blank=False, editable=False, auto_now=True)
    createAt = models.DateTimeField(null=False, blank=False, editable=False, auto_now_add=True)

    def __str__(self):
        return self.name

    def birthday(self):
        _date_of_birth = self.date_of_birth.strftime('%d/%m/%Y')
        return _date_of_birth
