from django.contrib.auth.views import LogoutView
from django.urls import path
from booker import views

urlpatterns = [
    path('', views.index, name='index'),
    path('all-bookings/', views.all_bookings, name='all-bookings'),
    path('profile/', views.profile, name='profile'),
    path('create-booking/', views.create_booking, name='create_booking'),
    path('my-bookings/', views.view_bookings, name='view_bookings'),
    path('delete-booking/<int:booking_id>/', views.delete_booking, name='delete_booking'),
    path('create-profile/', views.create_profile, name='create_profile'),
    # path('edit-profile/', views.edit_profile, name='edit_profile'),
    path('upload-profile-picture/', views.upload_profile_picture, name='upload_profile_picture'),
    path("update-phone-number/", views.update_phone_number, name="update_phone_number"),
    path('login/', views.login_view, name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('check-availability/', views.check_availability, name='check_availability')
    # debug url
    # path("test-login/", views.test_login_view, name='test_login')
]

LOGIN_URL = '/'

# this is disabled due to security issues
# LOGOUT_REDIRECT_URL = '/'
