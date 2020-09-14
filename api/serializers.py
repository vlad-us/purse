from rest_framework import serializers


from purse.models import SubCategory, BudgetEntry


class BudgetSerialiser(serializers.ModelSerializer):
    """Сериализатор для подтягивания категорий в ajax запрос при добавлении записи о расходе/доходе"""
    class Meta:
        model = SubCategory
        fields = ['name']


class BudgetEntryToExcelSerializer(serializers.ModelSerializer):
    """Сериализатор для формирования данных на экспорт в excel"""

    class Meta:
        model = BudgetEntry
        fields = ['title', 'type', 'amount', 'created_at']
