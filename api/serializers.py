from rest_framework import serializers


from purse.models import SubCategory


class BudgetSerialiser(serializers.ModelSerializer):
    """Сериализатор для подтягивания категорий в ajax запрос при добавлении записи о расходе/доходе"""
    class Meta:
        model = SubCategory
        fields = ['name']
