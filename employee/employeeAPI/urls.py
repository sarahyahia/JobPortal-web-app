from django.urls import path,include
from . import views

urlpatterns = [
    path('',views.get_emps),
    path('<int:pk>',views.get_emp),
    path('add',views.create_emp_profile),
    path('edit',views.edit_emp_profile),
    
]