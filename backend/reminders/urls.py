from django.urls import path
from . import views

urlpatterns = [
    path('', views.reminders_home, name='reminders_home'),
    path('add/', views.add_reminder, name='add_reminder'),
    path('edit/<int:pk>/', views.edit_reminder, name='edit_reminder'),
    path('delete/<int:pk>/', views.delete_reminder, name='delete_reminder'),
    path('toggle/<int:pk>/', views.toggle_reminder, name='toggle_reminder'),
    path('mark-taken/<int:pk>/<str:time_slot>/', views.mark_taken, name='mark_taken'),
]
