from datetime import date, datetime, timedelta

from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.views.decorators.http import require_GET

from appointment.models import Appointment


@require_GET
@login_required
def show_total_values(request):
    appointments = Appointment.objects.all().count()
    return appointments


@require_GET
@login_required
def show_total_values_today(request):
    appointments = Appointment.objects.filter(date_appointment__startswith=date.today()).count()
    return appointments


@login_required
def show_total_values_month(request):
    appointments = Appointment.objects.filter(
        date_appointment__lte=datetime.now() + timedelta(days=30)
    ).count()
    return appointments


@login_required
def show_total_values_last_month(request):
    appointments = Appointment.objects.filter(
        date_appointment__lt=datetime.today() - timedelta(days=60)
    ).count()
    return appointments


@login_required
def home(request):
    context = {
        "show_total_values": show_total_values(request),
        "show_total_values_today": show_total_values_today(request),
        "show_total_values_month": show_total_values_month(request),
        "show_total_values_last_month": show_total_values_last_month(request),
    }
    return render(request, "home.html", context)
