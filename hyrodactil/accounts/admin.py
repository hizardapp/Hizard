from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from .forms import UserCreationForm
from .models import CustomUser


class CustomUserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = CustomUser

    def clean_password(self):
        return self.initial["password"]


class CustomUserAdmin(UserAdmin):
    add_form = UserCreationForm
    form = CustomUserChangeForm

    list_display = ('email', 'first_name', 'last_name', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)
    filter_horizontal = ('groups', 'user_permissions',)

    fieldsets = (
        (None, {'fields': ('email', 'password', 'first_name', 'last_name', 'avatar')}),
        ('Permissions', {'fields': ('is_active',
                                    'is_staff',
                                    'is_superuser',
                                    'groups',
                                    'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2', 'first_name', 'last_name', 'avatar')}
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
