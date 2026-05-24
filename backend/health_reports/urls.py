from django.urls import path
from . import views

urlpatterns = [
    path('', views.reports_home, name='reports_home'),
    path('upload/', views.upload_report, name='upload_report'),
    path('<int:pk>/', views.report_detail, name='report_detail'),
    path('<int:pk>/delete/', views.delete_report, name='delete_report'),
]
