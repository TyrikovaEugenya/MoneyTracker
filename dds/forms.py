from django import forms
from .models import Transaction, Type, Category, Subcategory

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['created_at', 'status', 'type', 'category', 'subcategory', 'amount', 'comment']
        widgets = {
            'created_at': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'type' in self.data:
            try:
                type_id = int(self.data.get('type'))
                self.fields['category'].queryset = Category.objects.filter(type_id=type_id)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['category'].queryset = Category.objects.none()

        if 'category' in self.data:
            try:
                category_id = int(self.data.get('category'))
                self.fields['subcategory'].queryset = Subcategory.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                pass
        else:
            self.fields['subcategory'].queryset = Subcategory.objects.none()

        # Инициализация при редактировании
        if self.instance.pk:
            self.fields['category'].queryset = Category.objects.filter(type=self.instance.type)
            self.fields['subcategory'].queryset = Subcategory.objects.filter(category=self.instance.category)