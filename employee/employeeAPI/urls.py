from django.urls import path, include, re_path
from . import views

urlpatterns = [
    re_path('search', views.EmployeeList.as_view()),
    path('',views.get_emps),
    path('pl/',views.get_program_langs),
    path('emp/<int:pk>',views.get_emp),
    path('add',views.create_emp_profile),
    path('edit',views.edit_emp_profile),
    
]