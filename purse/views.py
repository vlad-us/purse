from django.views.generic.base import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
class IndexPageView(TemplateView):
    """Индексная страница, доступна всем"""
    template_name = 'purse/index_page.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Страница профиля, доступна авторизованным пользователям"""
    redirect_field_name = 'next'
    template_name = 'purse/profile.html'
