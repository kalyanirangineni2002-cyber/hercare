from django.urls import path
from . import views

urlpatterns = [
    path('', views.mental_health_home, name='mental_health_home'),
    path('log-mood/', views.log_mood, name='log_mood'),
    path('mood-history/', views.mood_history, name='mood_history'),
    path('resources/', views.resources, name='resources'),
]
