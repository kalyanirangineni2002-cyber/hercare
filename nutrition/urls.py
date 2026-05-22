from django.urls import path
from . import views

urlpatterns = [
    path('', views.nutrition_home, name='nutrition_home'),
    path('article/<int:pk>/', views.article_detail, name='article_detail'),
    path('fitness/', views.fitness_routines, name='fitness_routines'),
    path('fitness/<int:pk>/', views.routine_detail, name='routine_detail'),
]
