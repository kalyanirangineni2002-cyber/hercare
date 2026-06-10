from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
<<<<<<< HEAD
    path('terms/', views.terms_view, name='terms'),
    path('privacy/', views.privacy_view, name='privacy'),
=======
    path('terms/',views.terms_view,name='terms'),
    path('privacy/',views.privacy_view,name='privacy'),
>>>>>>> d7044ddf2cf7550a3942b7f0a2371ac5288cd461
]
