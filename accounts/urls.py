from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.login_page, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('settings/<str:un>', views.account_settings, name='settings'),
    path('messages/', views.user_messages, name='messages'),
    path('inbox/', views.view_inbox, name='inbox')
]
