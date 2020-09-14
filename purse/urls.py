from django.urls import path
from .views import *


app_name = 'purse'
urlpatterns = [
    path('', IndexPageView.as_view(), name='index'),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path('create/', AddBudgetEntry.as_view(), name='add_budget_entry'),
    path('profile/<int:user>/<int:year>/<str:slug>/', BudgetDetailView.as_view(), name='budget_detail'),
]
