from django.urls import path, include
from .views import authView, home
from . import views

urlpatterns = [
 path("", home, name="home"),
 path('login/', views.login, name='login'),
 path("signup/", authView, name="authView"),
 path("accounts/", include("django.contrib.auth.urls")),
 path('add_project/', views.add_project, name='add_project'),
 path('success/', views.success_view, name='success_view'),
 ]