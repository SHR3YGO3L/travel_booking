from django.urls import path
from . import views
from django.shortcuts import redirect
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib.auth import views as auth_views
urlpatterns = [
    path('register/', views.register, name='register'),

    path('travel/', views.travel_options, name='travel_options'),

    path('login/', auth_views.LoginView.as_view(template_name='booking/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='booking/logout.html',http_method_names=['get', 'post']), name='logout'),
    path('book/<int:travel_id>/', views.book_travel, name='book_travel'),
    path('cancel-booking/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('my-bookings/', views.my_bookings, name='my_bookings'),

    
    path('password-change/', auth_views.PasswordChangeView.as_view(template_name='booking/password_change.html', success_url='/'), name='password_change'),
    path('toggle-theme/', views.toggle_theme, name='toggle_theme'),
    path('password-change/done/', auth_views.PasswordChangeDoneView.as_view(template_name='booking/password_change_done.html'), name='password_change_done'),
]






