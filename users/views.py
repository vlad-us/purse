from django.shortcuts import render, get_object_or_404
from django.contrib.auth.views import (LoginView, LogoutView, PasswordChangeView, PasswordResetView,
                                       PasswordResetConfirmView, PasswordResetCompleteView)
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, TemplateView
from django.views.generic.edit import UpdateView
from django.urls import reverse_lazy
from django.core.signing import BadSignature
from django.contrib.messages.views import SuccessMessageMixin


from .forms import *
from .utils import signer
from .models import *


# Create your views here.
class UserLoginView(LoginView):
    redirect_authenticated_user = True
    form_class = CustomUserLoginForm
    template_name = 'users/login.html'


class UserLogoutView(LogoutView):
    next_page = 'purse:index'


class UserChangeInfo(SuccessMessageMixin, LoginRequiredMixin, UpdateView):
    """Изменение данных пользователя"""
    model = CustomUser
    template_name = 'users/change_user_info.html'
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('purse:profile')
    success_message = 'Личные данные пользователя обновлены'

    def dispatch(self, request, *args, **kwargs):
        self.user_id = request.user.pk
        return super().dispatch(request, *args, **kwargs)

    def get_object(self, queryset=None):
        if not queryset:
            queryset = self.get_queryset()
        return get_object_or_404(queryset, pk=self.user_id)


class UserPasswordChangeView(SuccessMessageMixin, LoginRequiredMixin, PasswordChangeView):
    """Контроллер смены пароля"""
    template_name = 'users/password_change.html'
    success_url = reverse_lazy('purse:profile')
    form_class = CustomUserPasswordChangeForm
    success_message = 'Пароль успешно изменен.'


class UserPasswordResetView(SuccessMessageMixin, PasswordResetView):
    """Контроллер для сброса забытого/утерянного пароля"""
    template_name = 'users/password_reset.html'
    subject_template_name = 'email/reset_subject.txt'
    email_template_name = 'email/reset_email.txt'
    success_url = reverse_lazy('purse:index')
    success_message = 'Письмо со ссылкой для сброса пароля отправлено на указанный email.'
    form_class = CustomUserPasswordResetForm


class UserPasswordResetConfirmView(SuccessMessageMixin, PasswordResetConfirmView):
    """Контроллер для задания нового пароля после сброса"""
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('users:password_reset_complete')
    form_class = CustomUserSetNewPasswordForm


class UserPasswordResetCompleteView(PasswordResetCompleteView):
    """Выводит страницу с сообщеием об успешной смене пароля после сброса"""
    template_name = 'users/password_reset_complete.html'


class UserRegistrationView(SuccessMessageMixin, CreateView):
    model = CustomUser
    template_name = 'users/user_registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('purse:index')
    success_message = 'Пользователь зарегистрирован. Письмо с ссылкой для активации аккаунта отправлено на email, ' \
                      'указанный при регистрации'


class UserRegistrationDone(TemplateView):
    template_name = 'users/user_registration_done.html'


def user_activate(request, sign):
    try:
        username = signer.unsign(sign)
    except BadSignature:
        return render(request, 'users/bad_signature.html')
    user = get_object_or_404(CustomUser, email=username)
    if user.is_active:
        template = 'users/user_is_activated.html'
    else:
        template = 'users/activation_done.html'
        user.is_active = True
        user.save()
    return render(request, template)
