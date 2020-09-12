from django.views.generic.base import TemplateView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


from .models import BudgetEntry, AggregateBudget
from .forms import BudgetEntryForm
from users.models import CustomUser
from .services import details_per_category


# Create your views here.
class IndexPageView(TemplateView):
    """Индексная страница, доступна всем"""
    template_name = 'purse/index_page.html'


class UserProfileView(LoginRequiredMixin, TemplateView):
    """Страница профиля, доступна авторизованным пользователям"""
    template_name = 'purse/profile.html'

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['month_budgets'] = AggregateBudget.objects.filter(user=self.request.user)


class AddBudgetEntry(LoginRequiredMixin, CreateView):
    """Создание записи расхода/дохода"""
    template_name = 'purse/add_budget_entry.html'
    form_class = BudgetEntryForm
    success_url = reverse_lazy('purse:add_budget_entry')

    def get_initial(self):
        user = CustomUser.objects.get(email=self.request.user.email)
        return {'user': user}

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        extra_context = details_per_category(self.request.user)
        context.update(extra_context)
        return context
