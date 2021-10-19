from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from patient.views import updatePatient

from . import views

app_name = "patient"

urlpatterns = [
    path("patient-list/", views.patientList, name="patient-list"),
    path("show-details/<str:pk>", views.showDetails, name="show-details"),
    path("patient-register/", views.registerPatient, name="patient-register"),
    path("patient-update/<str:pk>", updatePatient, name="patient-update",),
]
