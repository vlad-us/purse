from django.db.models import Sum

from .models import AggregateBudget

MONTHS_MAPPING = {
    1: 'Январь', 2: 'Февраль', 3: 'Март', 4: 'Апрель', 5: 'Май', 6: 'Июнь',
    7: 'Июль', 8: 'Август', 9: 'Сентябрь', 10: 'Октябрь', 11: 'Ноябрь', 12: 'Декабрь'
}


def details_per_category(user):
    """
    Функция считает общую сумму затрат и доходов за месяц.
    сумму затрат и доходов по категориям. Написана для представления AddBudgetEntry.
    """
    try:
        # Получить последний агрегированный бюджет пользователя
        last_month_budget = AggregateBudget.objects.filter(user=user).last()
        month = MONTHS_MAPPING[last_month_budget.month]

        # Сортировка BudgetEntries на доход/расход
        income_budget_entries = last_month_budget.budgetentry_set.filter(type='i')
        expense_budget_entries = last_month_budget.budgetentry_set.filter(type='e')

        # Получить уникальные категории для дохода/расхода
        income_categories = [i.category for i in income_budget_entries.distinct('category_id').order_by('category_id')]
        expense_categories = [i.category for i in expense_budget_entries.distinct('category_id').order_by('category_id')]

        # Посчитать общие суммы дохода/расхода
        if not income_budget_entries:
            total_income = {'amount__sum': 0}
        else:
            total_income = income_budget_entries.aggregate(Sum('amount'))
        if not expense_budget_entries:
            total_expense = {'amount__sum': 0}
        else:
            total_expense = expense_budget_entries.aggregate(Sum('amount'))
        print('total_income: ', total_income)
        print('total_expense: ', total_expense)

        # Посчитать суммы по каждой категории в отдельности
        expenses_per_category = {
            category.name: expense_budget_entries.filter(category=category).aggregate(Sum('amount'))['amount__sum'] for
            category in expense_categories}
        incomes_per_category = {
            category.name: income_budget_entries.filter(category=category).aggregate(Sum('amount'))['amount__sum'] for
            category in income_categories}
        balance = total_income['amount__sum'] - total_expense['amount__sum']
        context = {
            'total_income': total_income,
            'total_expense': total_expense,
            'expenses_per_category': expenses_per_category,
            'incomes_per_category': incomes_per_category,
            'balance': balance,
            'month': month
        }
        return context
    except AttributeError:
        return {}
