from django.urls import path
from booker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-bookings/', views.all_bookings, name='all-bookings'),
    path('profile/', views.profile, name='profile'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('create-profile/', views.create_profile, name='create_profile'),
    path('login/', views.login_view, name='login'),
]

LOGIN_URL = '/'
