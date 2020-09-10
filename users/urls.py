from django.urls import path
from .views import *


app_name = 'users'
urlpatterns = [
    # Вход/выход с сайта
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    # Изменить информацию о себе
    path('profile/change/', UserChangeInfo.as_view(), name='change_profile'),
    # Изменить пароля
    path('password/change/', UserPasswordChangeView.as_view(), name='password_change'),
    # Сброс пароля
    path('password/reset/', UserPasswordResetView.as_view(), name='password_reset'),
    path('password/reset/<uidb64>/<token>/', UserPasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('password/reset/done/', UserPasswordResetCompleteView.as_view(), name='password_reset_complete'),
    # Регистрация пользователя на сайте
    path('registration/', UserRegistrationView.as_view(), name='user_registration'),
    path('registration/activate/<str:sign>/', user_activate, name='registration_activate'),
    # path('registration/done/', UserRegistrationDone.as_view(), name='user_registration_done'),
]
