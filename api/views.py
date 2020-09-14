from rest_framework import status
from django.http import JsonResponse
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.views import APIView


from purse.models import SubCategory, AggregateBudget
from .serializers import BudgetSerialiser, BudgetEntryToExcelSerializer


# Create your views here.
class CustomTokenViewBase(TokenObtainPairView):
    """Изменен класс ответа на JsonResponse"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK, safe=False)


class CustomTokenRefreshView(TokenRefreshView):
    """Изменен класс ответа на JsonResponse"""
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return JsonResponse(serializer.validated_data, status=status.HTTP_200_OK, safe=False)


class CategoriesView(APIView):
    """Класс для ajax запроса в представлении"""
    def get(self, request, type):
        categories = SubCategory.objects.filter(type=type)
        serializer = BudgetSerialiser(categories, many=True)
        return JsonResponse(serializer.data, safe=False)


class BudgetEntriesToExcelView(APIView):
    """Класс для ajax запроса на выгрузку данных в excel"""
    def get(self, request, user, year, slug):
        data = AggregateBudget.objects.get(user=user, year=year, slug=slug)
        data = data.budgetentry_set.all()
        serializer = BudgetEntryToExcelSerializer(data, many=True)
        return JsonResponse(serializer.data, safe=False)
