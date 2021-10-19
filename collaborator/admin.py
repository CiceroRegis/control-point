from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from collaborator.models import Occupation

from .models import Profile


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False
    verbose_name_plural = _('Profile')
    fk_name = 'user'


class CustomUserAdmin(UserAdmin):
    inlines = (ProfileInline,)
    list_display = (
    'username', 'email', 'first_name', 'last_name', 'get_nome', 'get_birth_date', 'get_occupation', 'is_staff')
    list_select_related = ('profile',)

    def get_nome(self, instance):
        return instance.profile.nome

    get_nome.short_description = 'Nome'

    def get_birth_date(self, instance):
        return instance.profile.birth_date

    get_birth_date.short_description = 'Aniversário'

    def get_occupation(self, instance):
        return instance.profile.occupation

    get_occupation.short_description = 'Profissão'

    def get_inline_instances(self, request, obj=None):
        if not obj:
            return list()
        return super(CustomUserAdmin, self).get_inline_instances(request, obj)


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
admin.site.register(Profile)
admin.site.register(Occupation)