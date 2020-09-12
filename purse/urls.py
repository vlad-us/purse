from django.urls import path
from django.contrib.auth.decorators import login_required
from .views import *


app_name = 'purse'
urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    # path('profile/', UserProfileView.as_view(), name='profile'),
    path('profile/', AddBudgetEntry.as_view(), name='add_budget_entry')
]
