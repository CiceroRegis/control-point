import time

from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.translation import gettext_lazy as _
from django.views.decorators.debug import sensitive_post_parameters
from django.views.decorators.http import require_GET
from django.views.generic import CreateView, ListView, UpdateView

from collaborator.form import ProfileForm, UserForm
from collaborator.models import Profile, User


@login_required
def logout_view(request):
    logout(request)
    return redirect("collaborator:logout")


def registerCollaborator(request):
    user_form = UserForm()
    form = ProfileForm()
    if request.method == "POST":
        form = ProfileForm(request.POST)
        user_form = UserForm(request.POST)
        if form.is_valid() and user_form.is_valid():
            form.save()
            user_form.save()
            messages.success(request, _("Your profile was successfully Saved!"))
            return redirect("collaborator:logout")
        else:
            messages.warning(
                request, _("Please correct the error below."),
            )
    return render(
        request,
        "register/create_user_profile.html",
        {"form": form, "user_form": user_form},
    )


@login_required
@require_GET
def listCollaborators(request):
    search = request.GET.get('search')

    if search:
        profiles = Profile.objects.filter(nome__icontains=search)
    else:
        profiles = Profile.objects.all().order_by('nome')
        paginator = Paginator(profiles, 10)
        page = request.GET.get('page', 1)
        try:
            profiles = paginator.get_page(page)
        except PageNotAnInteger:
            profiles = paginator.get_page(1)
        except EmptyPage:
            profiles = paginator.get_page(paginator.num_pages)
    return render(request, "collaborator/collaborator_list.html", {'profiles': profiles})


@login_required
def updateProfile(request, pk):
    profile = Profile.objects.get(id=pk)
    if request.method == "POST":
        profile_form = ProfileForm(request.POST, instance=profile)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, _("Your profile was successfully updated!"))
            return redirect("collaborator:list-collaborator")
        else:
            messages.warning(request, _("Please correct the error below."))
    else:
        profile_form = ProfileForm(instance=profile)
    return render(
        request, "register/register_collaborator.html", {"form": profile_form}
    )


# @login_required
# @require_GET
# def disableProfileCollaborator(request, id):
#     c = Collaborator.objects.get(pk=collaborator)
#     if not c:
#         messages.warning(request, _("This Collaborator not found."))
#     try:
#         if c:
#             c.delete()
#             messages.success(request, _("Collaborator canceled."))
#     except Exception:
#         messages.warning(request, _("Collaborator not canceled."))

#     return redirect("collaborator:list-collaborator")


@login_required
@require_GET
def showProfile(request):
    context = {"profile": User.objects.filter(username=request.user)}
    return render(request, "collaborator/profile_user.html", context)
