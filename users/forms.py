from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm, AuthenticationForm, PasswordChangeForm,
                                       PasswordResetForm, SetPasswordForm)
from django.contrib.auth import password_validation
from django.contrib.auth.password_validation import (MinimumLengthValidator, get_default_password_validators,
                                                     validate_password)
from .models import CustomUser, user_registrated


class CustomUserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя"""
    username = forms.CharField(
        widget=forms.EmailInput(attrs={'autofocus': True, 'class': 'form-control', 'placeholder': 'Ваша почта'})
    )
    password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'class': 'form-control', 'placeholder': 'Ваш пароль'})
    )


class CustomUserChangeForm(forms.ModelForm):
    """Форма правки личных данных"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone', 'date_of_birth']


class CustomUserPasswordChangeForm(PasswordChangeForm):
    """Форма смены пароля"""
    old_password = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'current-password', 'autofocus': True, 'class': 'form-control',
                   'placeholder': 'Старый пароль'})
    )
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Новый пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html()
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Новый пароль еще раз'}),
        strip=False,
    )


class CustomUserPasswordResetForm(PasswordResetForm):
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Введите адрес электронной почты'})
    )


class CustomUserSetNewPasswordForm(SetPasswordForm):
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Новый пароль'}),
        strip=False,
        help_text=password_validation.password_validators_help_text_html(),
    )
    new_password2 = forms.CharField(
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Новый пароль еще раз'}),
    )


class UserRegistrationForm(forms.ModelForm):
    phone = forms.CharField(
        label='Номер телефона',
        widget=forms.TextInput(attrs={'id': 'phone'})
    )
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(
            attrs={'autocomplete': 'email', 'class': 'form-control', 'placeholder': 'Введите адрес электронной почты'}),
    )
    first_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Ваше имя'}
        )
    )
    last_name = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={'class': 'form-control', 'placeholder': 'Ваша фамилия'}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Пароль'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={'autocomplete': 'new-password', 'class': 'form-control', 'placeholder': 'Подтвердите пароль'}),
        help_text='Введите пароль еще раз для проверки',
    )

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone']

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Введенные пароли не совпадают.')
        return validate_password(cd['password2'])

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        user.is_active = False
        if commit:
            user.save()
        user_registrated.send(UserRegistrationForm, instance=user)
        return user
