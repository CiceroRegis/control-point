from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from collaborator.models import Occupation, Profile


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(
        widget=forms.PasswordInput
    )


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    username = forms.CharField(
        error_messages={"required": _("Username is required")},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "username"}
        ),
    )
    email = forms.EmailField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Email'}), )

    password = forms.CharField(
        error_messages={'required': _('Password is required')},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Senha'}),
    )
    confirm_password = forms.CharField(
        error_messages={'required': _('Comfirm password is required')},
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirmar Senha'}),
    )


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        exclude = ('user', "updateAt", "createAt",)

    nome = forms.CharField(
        error_messages={"required": _("Name is required")},
        widget=forms.TextInput(
            attrs={"class": "form-control", "placeholder": "Nome completo"}
        ),
    )

    birth_date = forms.DateField(
        input_formats=["%d/%m/%Y"],
        error_messages={
            "required": _("date of birth is required")
        },
        widget=forms.DateInput(
            attrs={
                "class": "form-control",
                "autocomplete": "off",
                "id": "birth_date",
                "placeholder": "Data de nascimento",
            }
        ),
    )

    cpf = forms.CharField(
        error_messages={"required": _("CPF is required")},
        widget=forms.TextInput(
            attrs={"class": "form-control", "id": "CPF", "placeholder": "CPF"}
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
    isWhatsapp = forms.BooleanField(required=False)

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

    SEXO_CHOICES = (
        ('M', _('Male')),
        ('F', _('Female')),
    )

    sexo = forms.ChoiceField(
        choices=SEXO_CHOICES, required=True, label='Sexo',
        error_messages={"required": _("Gender field is required")},
        widget=forms.Select(
            attrs={"name": "select_0", "class": "form-control", "placeholder": "Telefone Fixo"}
        ),
    )

    occupation = forms.ModelChoiceField(
        error_messages={"required": _("Occupation field is required")},
        widget=forms.Select(attrs={"class": "form-control", "placeholder": "Profissão", }
                            ),
        queryset=Occupation.objects.all()
    )
