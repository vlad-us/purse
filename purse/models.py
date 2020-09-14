from django.db import models
from uuid import uuid4
from pytils.translit import slugify
from users.models import CustomUser
from datetime import datetime
from django.urls import reverse


# Create your models here.
class BudgetCategory(models.Model):
    """Базовая модель категории расходов"""
    TYPES = (
        ('i', 'Доход'),
        ('e', 'Расход')
    )

    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, db_index=True, verbose_name='id')
    type = models.CharField(max_length=1, choices=TYPES, verbose_name='Тип')
    name = models.CharField(max_length=155, verbose_name='Категория')
    description = models.CharField(max_length=255, verbose_name='Описание')
    slug = models.SlugField(max_length=155)
    super_category = models.ForeignKey('SuperCategory', on_delete=models.PROTECT, null=True, blank=True, related_name='sub_categories')

    def save(self, commit=False, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super(BudgetCategory, self).save(*args, **kwargs)


class SuperCategoryManager(models.Manager):
    """Менеджер надкатегорий"""
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=True)


class SuperCategory(BudgetCategory):
    """Модель надкатегории"""
    objects = SuperCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = 'Надкатегория'
        verbose_name_plural = 'Надкатегории'


class SubCategoryManager(models.Manager):
    """Менеджер подкатегории"""
    def get_queryset(self):
        return super().get_queryset().filter(super_category__isnull=False)


class SubCategory(BudgetCategory):
    """Модель подкатегории"""
    objects = SubCategoryManager()

    def __str__(self):
        return self.name

    class Meta:
        proxy = True
        verbose_name = 'Подкатегория'
        verbose_name_plural = 'Подкатегории'


class AggregateBudget(models.Model):
    """Аггрегированный бюджет за месяц"""
    MONTHS = {
        1: 'January', 2: 'February', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'August', 9: 'September', 10: 'October', 11: 'November', 12: 'December'
    }

    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, db_index=True, verbose_name='id')
    month = models.PositiveSmallIntegerField(verbose_name='Месяц')
    year = models.PositiveSmallIntegerField(verbose_name='Год')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь')
    income_amount = models.PositiveIntegerField(verbose_name='Сумма дохода', default=0)
    expenses_amount = models.PositiveIntegerField(verbose_name='Сумма расхода', default=0)
    slug = models.SlugField(max_length=155)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Агрегированный бюджет за месяц'
        verbose_name_plural = 'Агрегированные бюджеты за месяц'
        ordering = ['-created_at']

    def save(self, commit=False, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.MONTHS[self.month])
        super(AggregateBudget, self).save(*args, **kwargs)

    def get_absolute_url(self):
        user = self.user.pk
        return reverse('purse:budget_detail', kwargs={'user': user, 'year': self.year, 'slug': self.slug})

    def get_api_url(self):
        user = self.user.pk
        url = 'http://127.0.0.1:8000' + reverse('api:export_to_excel', kwargs={'user': user, 'year': self.year, 'slug': self.slug})
        return url


class BudgetEntry(models.Model):
    """Запись о доходе/расходе"""
    TYPES = (
        ('i', 'Доход'),
        ('e', 'Расход')
    )

    id = models.UUIDField(unique=True, default=uuid4, primary_key=True, db_index=True, verbose_name='id')
    title = models.CharField(max_length=155, verbose_name='Заголовок')
    type = models.CharField(max_length=1, choices=TYPES, verbose_name='Тип')
    category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, verbose_name='Категория')
    amount = models.PositiveIntegerField(verbose_name='Сумма')
    day = models.PositiveIntegerField(verbose_name='Число', blank=True) #
    month = models.PositiveIntegerField(verbose_name='Месяц', blank=True) #
    year = models.PositiveIntegerField(verbose_name='Год', blank=True) #
    week_number = models.PositiveIntegerField(verbose_name='Номер недели', blank=True) #
    day_of_week = models.PositiveIntegerField(verbose_name='День недели', blank=True) #
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True)
    parent = models.ForeignKey(AggregateBudget, on_delete=models.CASCADE, verbose_name='Агрегированный бюджет', blank=True)
    created_at = models.DateTimeField(verbose_name='Дата создания', blank=True)
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления', blank=True)

    class Meta:
        verbose_name = 'Запись о расходе/доходе'
        verbose_name_plural = 'Записи о расходе/доходе'
        ordering = ['-created_at']

    def save(self, commit=False, *args, **kwargs):
        """Говнокод((( надо будет вынести в отдельную функцию"""
        self.created_at = datetime.now()
        self.day = self.created_at.day
        self.month = self.created_at.month
        self.year, self.week_number, self.day_of_week = self.created_at.isocalendar()
        try:
            aggr = AggregateBudget.objects.get(month=self.month, year=self.year, user=self.user)
            self.parent = aggr
            if self.type == 'i':
                aggr.income_amount += self.amount
            else:
                aggr.expenses_amount += self.amount
            aggr.save()
        except Exception:
            if self.type == 'i':
                aggr = AggregateBudget.objects.create(
                    month=self.month,
                    year=self.year,
                    income_amount=self.amount,
                    expenses_amount=0,
                    user=self.user
                )
                self.parent = aggr
            else:
                aggr = AggregateBudget.objects.create(
                    month=self.month,
                    year=self.year,
                    income_amount=0,
                    expenses_amount=self.amount,
                    user=self.user
                )
                self.parent = aggr
        super(BudgetEntry, self).save(*args, **kwargs)
