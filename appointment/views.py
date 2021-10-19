import logging

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET

from appointment.admin import Appointment
from appointment.form import AppointmentForm, FilterForm
from appointment.models import Appointment

logger = logging.getLogger("django")


@login_required
def create_appointment(request):
    form = AppointmentForm()
    if request.method == "POST":
        form = AppointmentForm(request.POST)
    try:
        if form.is_valid():
            form.save()
            messages.success(request, _("Appointment was successfully created!"))
            return redirect("appointments:list-appointments")
        else:
            context = {"form": form}
            return render(request, "appointment/create-appointments.html", context)
    except Exception:
        messages.warning(request, _("Error Form"))


@require_GET
@login_required
def show_total_values(request):
    appointments = Appointment.objects.all()
    return appointments


@login_required
def list_appointment(request):
    form_filter = {}
    search = request.GET.get("search")
    big_filter = FilterForm(request.GET)

    if big_filter.is_valid():
        form_filter = big_filter.cleaned_data
    if form_filter.get("date_appointment"):
        appointments = Appointment.objects.filter(date_appointment=form_filter.get("date_appointment")
            ).annotate(total=Sum("type_appointment__price"))

    elif search:
        appointments = Appointment.objects.filter(patient__name__icontains=search
        ).annotate(total=Sum("type_appointment__price"))
    else:
        appointments = (
            Appointment.objects.all().annotate(total=Sum("type_appointment__price"))
            .order_by("patient")
        )

        paginator = Paginator(appointments, 5)
        page = request.GET.get("page", 1)
        try:
            appointments = paginator.get_page(page)
        except PageNotAnInteger:
            appointments = paginator.get_page(2)
        except EmptyPage:
            appointments = paginator.get_page(paginator.num_pages)
    context = {
        "appointments": appointments,
        "show_total_values": show_total_values(request),
    }
    return render(request, "appointment/list-appointments.html", context)


@login_required
def update_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    if request.method == "POST":
        form = AppointmentForm(request.POST, instance=appointment)
        if form.is_valid():
            form.save()
            messages.success(request,_("Dados da consulta de {0} foi atualizada com sucesso!".format(
                        appointment.patient)),
            )
            return redirect("appointments:list-appointments")
        else:
            messages.warning(request, _("Please correct the error below."))
    else:
        form = AppointmentForm(instance=appointment)
        context = {"form": form}
        return render(request, "appointment/create-appointments.html", context)


@require_GET
@login_required
def start_consultation(request, pk):
    a = Appointment.objects.get(id=pk)

    if not a.consulting:
        a.consulting = True
        a.save()
        messages.success(
            request, _("A consulta com o (a) {0} foi iniciada ".format(a.patient))
        )
    else:
        a.consulting = False
        a.save()
        messages.success(
            request, _("A consulta com o (a) {0} foi finalizada".format(a.patient))
        )
    return redirect("appointments:list-appointments")
