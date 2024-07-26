# urls.py
from django.urls import path
from django.contrib.auth import views as auth_views
from .views import index, chat_view, message_list_create_view, register, user_list, send_message

urlpatterns = [
    path('', index, name='index'),
    path('home/', chat_view, name='home'),
    path('chat/<str:username>/', chat_view, name='chat_view'),
    path('messages/', message_list_create_view, name='message_list_create'),
    path('register/', register, name='register'),
    path('users/', user_list, name='user_list'),
    path('send-message/', send_message, name='send_message'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='registration/logout.html'), name='logout'),
]
