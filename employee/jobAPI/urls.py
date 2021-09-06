from django.urls import path, include, re_path
from . import views


urlpatterns = [
    re_path('search', views.JobList.as_view()),
    path('',views.get_jobs),
    path('<int:pk>',views.get_job),
    path('add',views.create_job),
    path('delete/<int:pk>',views.delete_job),   

    path('applicants/add',views.apply_job),
    path('applicants/<int:job_id>',views.get_applicants),
    path('applicants/status/<int:job_id>',views.edit_applicant_status),
    
]