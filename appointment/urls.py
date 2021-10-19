from django.conf import settings
from django.contrib.auth import views as auth_views
from django.urls import path

from . import views

app_name = "appointments"

urlpatterns = [
    path("list-appointments/", views.list_appointment, name="list-appointments"),
    path("create-appointment/", views.create_appointment, name="create-appointment"),
    path("update-appointment/<str:pk>", views.update_appointment, name="update-appointment",),
    path("appointment/<str:pk>/start-consultation", views.start_consultation, name="start-consultation"),
#     path("show-details/<str:pk>", views.showDetails, name="show-details"),

]
