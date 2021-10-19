from django.contrib import admin

from patient.form import PatientForm
from patient.models import Patient


# Register your models here.

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    model = PatientForm
    list_display = ('name', 'medical_record_number', 'phone_number', 'landline', 'email', 'address', 'birthday', 'sexo')
