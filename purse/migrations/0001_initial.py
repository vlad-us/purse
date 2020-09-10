# Generated by Django 3.0.4 on 2020-09-09 18:09

from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AggregateBudget',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('month', models.PositiveSmallIntegerField(verbose_name='Месяц')),
                ('year', models.PositiveSmallIntegerField(verbose_name='Год')),
                ('income_amount', models.PositiveIntegerField(verbose_name='Сумма дохода')),
                ('expenses_amount', models.PositiveIntegerField(verbose_name='Сумма расхода')),
                ('slug', models.SlugField(max_length=155)),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
            ],
            options={
                'verbose_name': 'Агрегированный бюджет за месяц',
                'verbose_name_plural': 'Агрегированные бюджеты за месяц',
                'ordering': ['-created_at'],
            },
        ),
        migrations.CreateModel(
            name='BudgetCategory',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('name', models.CharField(max_length=155, verbose_name='Категория')),
                ('description', models.CharField(max_length=255, verbose_name='Описание')),
                ('slug', models.SlugField(max_length=155)),
            ],
        ),
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True)),
                ('request_method', models.CharField(blank=True, max_length=155, null=True)),
                ('remote_addr', models.CharField(blank=True, max_length=155, null=True)),
                ('path_info', models.TextField(blank=True, null=True)),
                ('content_type', models.CharField(blank=True, max_length=155, null=True)),
                ('http_user_agent', models.CharField(blank=True, max_length=155, null=True)),
                ('user', models.CharField(blank=True, max_length=155, null=True)),
                ('status_code', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('reason_phrase', models.CharField(blank=True, max_length=155, null=True)),
                ('user_errors', models.TextField(blank=True, null=True)),
                ('begin_date', models.DateTimeField(blank=True, null=True)),
                ('duration', models.FloatField(blank=True, null=True)),
                ('exc_type', models.CharField(blank=True, max_length=155, null=True)),
                ('exc_value', models.TextField(blank=True, null=True)),
                ('exc_traceback', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='BudgetEntry',
            fields=[
                ('id', models.UUIDField(db_index=True, default=uuid.uuid4, primary_key=True, serialize=False, unique=True, verbose_name='id')),
                ('type', models.CharField(choices=[('i', 'income'), ('e', 'expense')], max_length=1, verbose_name='Тип')),
                ('amount', models.PositiveIntegerField(verbose_name='Сумма')),
                ('day', models.PositiveIntegerField(blank=True, verbose_name='Число')),
                ('month', models.PositiveIntegerField(blank=True, verbose_name='Месяц')),
                ('year', models.PositiveIntegerField(blank=True, verbose_name='Год')),
                ('week_number', models.PositiveIntegerField(blank=True, verbose_name='Номер недели')),
                ('day_of_week', models.PositiveIntegerField(blank=True, verbose_name='День недели')),
                ('created_at', models.DateTimeField(blank=True, verbose_name='Дата создания')),
                ('updated_at', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('parent', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='purse.AggregateBudget', verbose_name='Агрегированный бюджет')),
            ],
            options={
                'verbose_name': 'Запись о расходе/доходе',
                'verbose_name_plural': 'Записи о расходе/доходе',
                'ordering': ['-created_at'],
            },
        ),
    ]