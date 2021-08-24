from django.contrib import admin
from .models import Employee, Job, ProgrammingLanguage, JobApplicant

# Register your models here.
admin.site.register(Employee)
admin.site.register(Job)
admin.site.register(ProgrammingLanguage)
# admin.site.register(Employer)
admin.site.register(JobApplicant)

