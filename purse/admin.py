from django.contrib import admin
from .models import SubCategory, SuperCategory, AggregateBudget, BudgetEntry


class SubCategoryInline(admin.TabularInline):
    model = SubCategory
    prepopulated_fields = {'slug': ('name', )}


@admin.register(SubCategory)
class SubCategoryAdmin(admin.ModelAdmin):
    model = SubCategory


@admin.register(SuperCategory)
class SuperCategoryAdmin(admin.ModelAdmin):
    model = SuperCategory
    prepopulated_fields = {'slug': ('name',)}
    inlines = [SubCategoryInline, ]


@admin.register(BudgetEntry)
class BudgetEntryAdmin(admin.ModelAdmin):
    model = BudgetEntry
