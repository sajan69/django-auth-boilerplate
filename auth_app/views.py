from django.shortcuts import render, redirect
from django.views.generic.edit import FormView
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout, get_user_model
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from .models import OTP, CustomUser
from .forms import CustomerRegistrationForm, AdminRegistrationForm, OTPVerificationForm, LoginForm


class CustomerRegistrationView(FormView):
    template_name = 'auth_app/register_customer.html'
    form_class = CustomerRegistrationForm

    def form_valid(self, form):
        user = form.save()
        otp = OTP(user=user)
        otp.generate_otp_code()
        otp.save()
        # Send OTP to user's email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('otp_verify', user_id=user.id)

class AdminRegistrationView(FormView):
    template_name = 'auth_app/register_admin.html'
    form_class = AdminRegistrationForm

    def form_valid(self, form):
        user = form.save()
        otp = OTP(user=user)
        otp.generate_otp_code()
        otp.save()
        # Send OTP to user's email
        send_mail(
            'Your OTP Code',
            f'Your OTP code is {otp.otp_code}',
            'from@example.com',
            [user.email],
            fail_silently=False,
        )
        return redirect('otp_verify', user_id=user.id)

from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.contrib.auth import login as auth_login
from .models import OTP

class OTPVerificationView(FormView):
    template_name = 'auth_app/otp_verify.html'
    form_class = OTPVerificationForm

    def form_valid(self, form):
        user_id = self.kwargs['user_id']
        otp_code = form.cleaned_data['otp_code']
        try:
            otp = OTP.objects.get(user_id=user_id, otp_code=otp_code, is_verified=False)
            if otp.is_expired():
                return redirect('otp_resend', user_id=user_id)
            otp.is_verified = True
            otp.save()
            
            # Retrieve the user instance
            User = get_user_model()  # Using get_user_model to handle custom user model
            user = User.objects.get(pk=user_id)
            
            # Authenticate and log in the user
            auth_login(self.request, user)
            
            return redirect('home')
        except OTP.DoesNotExist:
            form.add_error(None, 'Invalid OTP code')
            return self.form_invalid(form)


class LoginView(FormView):
    template_name = 'auth_app/login.html'
    form_class = LoginForm

    def form_valid(self, form):
        username = form.cleaned_data['username']
        password = form.cleaned_data['password']
        user = authenticate(username=username, password=password, backend='django.contrib.auth.backends.ModelBackend')

        if user is not None:
            auth_login(self.request, user)
            return redirect('home')
        else:
            form.add_error(None, 'Invalid login credentials')
            return self.form_invalid(form)

class PasswordChangeView(FormView):
    template_name = 'auth_app/password_change.html'
    form_class = PasswordChangeForm

    def form_valid(self, form):
        old_password = form.cleaned_data['old_password']
        new_password = form.cleaned_data['new_password1']
        user = self.request.user
        if user.check_password(old_password):
            user.set_password(new_password)
            user.save()
            # Optionally, send an email notification about the password change
            send_mail(
                'Password Changed',
                'Your password has been changed successfully.',
                'from@example.com',
                [user.email],
                fail_silently=False,
            )
            return redirect('login')
        else:
            form.add_error(None, 'Incorrect old password')
            return self.form_invalid(form)

def logout_view(request):
    auth_logout(request)
    return redirect('login')