from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Employee, Job, ProgrammingLanguage, JobApplicant, User, Employer


class MyUserAdmin(UserAdmin):
    model = User
    ordering = ('email',)
    list_display = ('email', 'date_joined', 'last_login', 'is_admin', 'is_staff')
    search_fields = ('email',)
    readonly_fields = ('date_joined', 'last_login')
    add_fieldsets = (
        (None, {'fields': ('email',"password","password2","isEmployer", 'first_name', 'last_name', )}),
    )
    fieldsets = (
        (None, {
            "fields": (
                ('email', 'first_name', 'last_name','is_staff',)
                
            ),
        }),
    )

# Register your models here.
admin.site.register(Employee)
admin.site.register(Employer)
admin.site.register(User, MyUserAdmin)
admin.site.register(Job)
admin.site.register(ProgrammingLanguage)
admin.site.register(JobApplicant)
