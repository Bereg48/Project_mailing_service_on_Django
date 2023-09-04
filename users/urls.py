from django.urls import path, reverse_lazy
from django.views.generic import TemplateView
from django.contrib.auth.views import (PasswordResetView,
                                       PasswordResetDoneView,
                                       PasswordResetConfirmView,
                                       PasswordResetCompleteView)

from users.apps import UsersConfig
from users.views import LogoutView, LoginView, RegisterView, EmailVerify

app_name = UsersConfig.name

urlpatterns = [
    path('', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('password_reset/', PasswordResetView.as_view(template_name='users/password_reset.html' ,success_url=reverse_lazy('users:password_reset_done'), html_email_template_name='users/password_reset_email.html'), name='password_reset'),
    path('password_reset_done/', PasswordResetDoneView.as_view(template_name='users/password_reset_done.html'), name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html', success_url=reverse_lazy('users:password_reset_complete')), name='password_reset_confirm'),
    path('password_reset_complete/', PasswordResetCompleteView.as_view(template_name='users/login.html'), name='password_reset_complete'),
    path('invalid_verify/', TemplateView.as_view(template_name='users/invalid_verify.html'), name='invalid_verify'),
    path('confirm_email/', TemplateView.as_view(template_name='users/confirm_email.html'), name='confirm_email'),
    path('verify_email/<uidb64>/<token>/', EmailVerify.as_view(), name='verify_email'),

]
