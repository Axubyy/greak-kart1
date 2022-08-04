from . import views
from django.urls import path

urlpatterns = [
    path('register/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('logout/', views.logout, name="logout"),
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('', views.dashboard, name='dashboard'),
    path('forgot-password/', views.forgot_password, name="forgot-password"),
    path('reset-password-validate/<uidb64>/<token>/',
         views.reset_password_validate, name="reset-password-validate"),
    path('reset-password', views.reset_password, name="reset-password"),
    path('edit-profile', views.edit_profile, name="edit-profile")
]
