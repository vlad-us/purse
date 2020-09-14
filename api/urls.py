from django.urls import path
from .views import *

app_name = 'api'
urlpatterns = [
    # jwt auth
    path('auth/token-pair/', CustomTokenViewBase.as_view(), name='token_pair'),
    path('auth/token-refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    # views
    path('ajax/categories/<str:type>/', CategoriesView.as_view()),
    path('ajax/<int:user>/<int:year>/<str:slug>/', BudgetEntriesToExcelView.as_view(), name='export_to_excel')
]
