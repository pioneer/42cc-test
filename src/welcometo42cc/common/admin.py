from django.contrib.auth.admin import UserAdmin
from django.contrib import admin

UserAdmin.fieldsets += (
    ('Extra info', {'fields': ('biography', 'birthdate', 'contacts')}),
    )
