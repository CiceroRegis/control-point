from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.shortcuts import redirect, render
from django.utils.translation import gettext_lazy as _
from django.views.decorators.http import require_GET

from patient.form import PatientForm
from patient.models import Patient


@login_required
def registerPatient(request):
    form = PatientForm()
    if request.method == 'POST':
        form = PatientForm(request.POST, request.FILES)
    try:
        if form.is_valid():
            form.save()
            form = PatientForm()
            messages.success(request, _("Patient was successfully Saved!"))
            return redirect("patient:patient-list")
        else:
            context = {'form': form}
            return render(request, 'patient/patient-register.html', context)
    except Exception:
        messages.warning(request, _('Error Form'))


@login_required
def updatePatient(request, pk):
    patient = Patient.objects.get(id=pk)
    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _("Patient was successfully updated!"))
            return redirect("patient:patient-list")
        else:
            messages.warning(request, _("Please correct the error below."))
    else:
        form = PatientForm(instance=patient)

        context = {

            "form": form,
        }
    return render(request, "patient/patient-register.html", context)


@require_GET
def show_total_values(request):
    patients = Patient.objects.all()
    return patients


@login_required
@require_GET
def patientList(request):
    search = request.GET.get('search')

    if search:
        patients = Patient.objects.filter(name__icontains=search)
    else:
        patients = Patient.objects.all().order_by('name')
        paginator = Paginator(patients, 10)
        page = request.GET.get('page', 1)
        try:
            patients = paginator.get_page(page)
        except PageNotAnInteger:
            patients = paginator.get_page(2)
        except EmptyPage:
            patients = paginator.get_page(paginator.num_pages)
        context = {'patients': patients,
                   'show_total_values': show_total_values(request)}
    return render(request, "patient/patient-list.html", context)


@login_required
@require_GET
def researchField(request, name):
    context = {'researchField': Patient.objects.filter(pacient__name_icontains=name)}
    return render(request, 'patient/show-details.html', context)


@login_required
@require_GET
def showDetails(request, pk):
    context = {'showDetails': Patient.objects.filter(id=pk)}
    return render(request, 'patient/show-details.html', context)
