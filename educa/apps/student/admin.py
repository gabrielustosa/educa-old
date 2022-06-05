from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from educa.apps.student.forms import UserCreateForm, UserEditForm
from educa.apps.student.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    add_form = UserCreateForm
    form = UserEditForm
    model = User
    list_display = ('name', 'email')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Informações pessoais', {'fields': ('name',)}),
        ('Permissões', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Datas Importantes', {'fields': ('last_login', 'date_joined')}),
    )
