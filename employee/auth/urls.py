from . import views 
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

urlpatterns = [
      # logout
      path("logout/", views.Logout.as_view()),
      path("login/", views.login_view),
      path('signup',views.signup_view),
      path("login/", obtain_auth_token),
      
]