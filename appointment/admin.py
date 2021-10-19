from django.contrib import admin

# Register your models here.
from appointment.models import Appointment, TypeAppointment, NotificationPatient


@admin.register(TypeAppointment)
class TypeAppointment(admin.ModelAdmin):
    model = TypeAppointment
    list_display = ('name', 'skip', 'price')


@admin.register(Appointment)
class Appointment(admin.ModelAdmin):
    model = Appointment
    # readonly_fields = ('patient', 'professional','type_appointment', 'createAt')
    list_display = ('patient', 'professional', 'date_appointment', 'createAt')
    filter_horizontal = ['type_appointment']


@admin.register(NotificationPatient)
class NotificationPacientAdmin(admin.ModelAdmin):
    pass