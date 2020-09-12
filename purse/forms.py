from django import forms


from .models import BudgetEntry


class BudgetEntryForm(forms.ModelForm):
    """Форма для создания записи о доходе/расходе"""

    class Meta:
        model = BudgetEntry
        fields = ['title', 'type', 'category', 'amount', 'user']
        widgets = {
            'user': forms.HiddenInput,
            'title': forms.TextInput(attrs={'class': 'form-control form-control-sm'}),
            'type': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'category': forms.Select(attrs={'class': 'form-control form-control-sm'}),
            'amount': forms.TextInput(attrs={'class': 'form-control form-control-sm'})
        }
