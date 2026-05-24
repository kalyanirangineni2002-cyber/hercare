from django.urls import path
from . import views

urlpatterns = [
    path('', views.tracker_home, name='tracker_home'),
    path('log/', views.log_period, name='log_period'),
    path('history/', views.cycle_history, name='cycle_history'),
    path('delete/<int:pk>/', views.delete_cycle_log, name='delete_cycle_log'),
]
