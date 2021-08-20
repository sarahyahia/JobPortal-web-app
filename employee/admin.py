from django.contrib import admin
from .models import Employee, Job, ProgrammingLanguage

# Register your models here.
admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(ProgrammingLanguage)
