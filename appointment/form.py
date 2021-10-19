from django import forms
from django.utils.translation import gettext_lazy as _

from appointment.models import Appointment, TypeAppointment
from collaborator.models import Profile
from patient.models import Patient


class FilterForm(forms.Form):
    date_appointment = forms.DateTimeField(required=True)


class AppointmentForm(forms.ModelForm):
    class Meta:
        model = Appointment
        exclude = (
            "updateAt",
            "createAt",
        )

    description = forms.CharField(
            error_messages={"required": _("Name appointment is required")},
            widget=forms.TextInput(
                attrs={"class": "form-control", "placeholder": "Informe a descrição do Atendimento"}
            ),
        )

    type_appointment = forms.ModelMultipleChoiceField(
        error_messages={"required": _("type appointment is required")},
        widget=forms.SelectMultiple(
            attrs={
                "class": "form-control js-example-basic-multiple",
                "name": "type_appointment[]",
                "multiple": "multiple",
            }
        ),
        required=False,
        queryset=TypeAppointment.objects.all(),
    )

    patient = forms.ModelChoiceField(
        widget=forms.Select(
            attrs={"class": "form-control js-example-placeholder-single"}
        ),
        queryset=Patient.objects.all()
    )

    professional = forms.ModelChoiceField(
        widget=forms.Select(attrs={"class": "form-control js-example-placeholder-single2"}),
        queryset=Profile.objects.all()
    )

    date_appointment = forms.DateTimeField(
        error_messages={"required": _("date appointment is required")},
        widget=forms.DateTimeInput(
            attrs={
                "class": "form-control datetimepicker",
                "autocomplete": "off",
                "placeholder": "Data da consulta",
            }
        ),
    )
