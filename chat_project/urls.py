from django.contrib import admin
from django.urls import path, include
from django.contrib.auth import views as auth_views
from chat import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),  # Home page
    path('home/', views.home, name='home'),
    path('chat/<str:username>/', views.chat_view, name='chat_view'),
    path('messages/', views.message_list_create_view, name='message_list_create'),
    path('register/', views.register, name='register'),
    path('user-list/', views.user_list, name='user_list'),
    # Authentication URLs
    path('accounts/login/', auth_views.LoginView.as_view(), name='login'),
    path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('accounts/password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('accounts/password_change/done/', auth_views.PasswordChangeDoneView.as_view(), name='password_change_done'),
    path('accounts/password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('accounts/password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('accounts/reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('accounts/reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
    # Include the chat app URLs
    path('api/', include('chat.urls')),
]
