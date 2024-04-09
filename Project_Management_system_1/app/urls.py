from django.contrib import admin
from django.urls import path
from . import views
from .views import DeleteView,CustomLoginView,RegisterPage,project_create, project_success, update_status_start, delete_project, dashboard_view 
from django.contrib.auth.views import LogoutView




urlpatterns = [
    
    path('',CustomLoginView.as_view(),name='login'),
    path('logout/',LogoutView.as_view(next_page='login'),name='logout'),
    path('register/',RegisterPage.as_view(), name='register'),
    path('create_project/', project_create, name='project_create'),
    path('success/', project_success, name='project_success'),
    path('update-status/start/<int:project_id>/', update_status_start, name='update_status_start'),
    path('update-status/close/<int:project_id>/', views.update_status_close, name='update_status_close'),
    path('update-status/cancel/<int:project_id>/', views.update_status_cancel, name='update_status_cancel'),
    path('delete-project/<int:project_id>/', delete_project, name='delete_project'),
    path('api/dashboard-counters/', views.dashboard_counters, name='dashboard_counters'),
    path('dashboard/', dashboard_view, name='dashboard'),
]