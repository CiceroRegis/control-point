from django.conf import settings
from django.contrib.auth import views as auth_views

from core.views import (
    logout_view,
    showProfile,
    listCollaborators,
    updateProfile,
)
from django.urls import path


app_name = "collaborator"

urlpatterns = [
    path("list-collaborator/", listCollaborators, name="list-collaborator"),
    path("update-profile-collaborator/<str:pk>", updateProfile, 
         name="update_profile_collaborator",
    ),
    # path("register/", login_page, name="register"),
    path("profile-user/", showProfile, name="profile_user"),
    path("accounts/login/", auth_views.LoginView.as_view(), name="login"),
    path("logout", logout_view, name="logout"),
    # path('logout/', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
]
