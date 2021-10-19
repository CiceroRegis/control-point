from django import forms
from django.utils.translation import gettext_lazy as _

from patient.models import Patient


class PatientForm(forms.ModelForm):
    class Meta:
        model = Patient
        exclude = (
            "updateAt",
            "createAt",
        )

    name = forms.CharField(
        error_messages={"required": _("name is required")},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Nome do paciente",
            }
        ),
    )

    medical_record_number = forms.IntegerField(
        required=False,
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "O número do prontuário é gerado automaticamente",
                   'readonly': 'True'}
        ),
    )

    email = forms.EmailField(
        widget=forms.TextInput(attrs={"class": "form-control", "placeholder": "Email"}),
    )

    photo = forms.FileField(
        widget=forms.ClearableFileInput(attrs={'id': 'photo', 'multiple': False, 'name': 'photo', 'value': 'Foto'}))

    date_of_birth = forms.DateField(
        input_formats=["%d/%m/%Y"],
        error_messages={"required": _("date of birth is required")},
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "id": "birth_date",
                "placeholder": "Data de nascimento",
            }
        ),
    )

    cpf_document = forms.CharField(
        error_messages={"required": _("CPF is required")},
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "CPF", "placeholder": "CPF"}
        ),
    )

    rg_document = forms.CharField(
        error_messages={"required": _("RG is required")},
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "RG", "placeholder": "RG"}
        ),
    )

    phone_number = forms.CharField(
        error_messages={"required": _("cell phone is required")},
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "phone_number",
                "placeholder": "Celular",
            }
        ),
    )

    landline = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "id": "landline",
                "placeholder": "Telefone Fixo",
            }
        ),
    )

    address = forms.CharField(
        required=False,
        widget=forms.TextInput(
            attrs={
                "class": "form-control",
                "placeholder": "Endereço",
            }
        ),
    )

    SEXO_CHOICES = (
        ("M", _("Male")),
        ("F", _("Female")),
    )

    sexo = forms.ChoiceField(
        choices=SEXO_CHOICES,
        required=True,
        label="Sexo",
        error_messages={"required": _("Gender field is required")},
        widget=forms.Select(
            attrs={
                "name": "select_0",
                "class": "form-control",
                "placeholder": "Telefone Fixo",
            }
        ),
    )
