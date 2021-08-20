from . import views 
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
      # logout
      path("logout/", views.Logout.as_view()),
      path('signup',views.api_signup),
      path("login/", obtain_auth_token),
      
]