from django.urls import path
from .views import CustomerRegistrationView, AdminRegistrationView, OTPVerificationView, LoginView, PasswordChangeView, logout_view

urlpatterns = [
    path('register/customer/', CustomerRegistrationView.as_view(), name='register_customer'),
    path('register/admin/', AdminRegistrationView.as_view(), name='register_admin'),
    path('otp/verify/<int:user_id>/', OTPVerificationView.as_view(), name='otp_verify'),
    path('login/', LoginView.as_view(), name='login'),
    path('password/change/', PasswordChangeView.as_view(), name='password_change'),
    path('logout/', logout_view, name='logout'),
]
