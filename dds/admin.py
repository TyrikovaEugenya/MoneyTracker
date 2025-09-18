from django import forms
from django.contrib import admin
from .models import Transaction

class TransactionAdmin(admin.ModelAdmin):
    class Meta:
        model = Transaction
        fields = '__all__'
        
    def clean(self):
        cleaned_data = super().clean()
        transaction_type = cleaned_data.get('type')
        transaction_category = cleaned_data.get('category')
        transaction_subcategory = cleaned_data.get('subcategory')
        
        # Проверка: категория должна быть привязана к типу
        if transaction_category and transaction_type and transaction_category.type != transaction_type:
            raise forms.ValidationError({
                "category": f"Категория '{transaction_category.name}' не относится к типу '{transaction_type.name}'."
            })
        
        # Проверка: подкатегория должна быть привязана к категории
        if transaction_subcategory and transaction_category and transaction_subcategory.category != transaction_category:
            raise forms.ValidationError({
                "subcategory": f"Подкатегория '{transaction_subcategory.name}' не относится к категории '{transaction_category.name}'."
            })

        return cleaned_data

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = (
        'created_at',
        'status',
        'type',
        'category',
        'subcategory',
        'amount',
        'comment_preview'
    )
    list_filter = (
        'created_at',
        'status',
        'type',
        'category',
        'subcategory'
    )
    search_fields = (
        'comment',
        'category__name',
        'subcategory__name'
    )
    date_hierarchy = 'created_at' # Иерархия дат — быстрый переход по календарю
    ordering = ['-created_at']
    # Группировка полей в форме редактирования
    fieldsets = (
        ('Основная информация', {
            'fields': ('created_at', 'status', 'type')
        }),
        ('Сумма и детали', {
            'fields': ('category', 'subcategory', 'amount', 'comment')
        }),
    )
    
    # Автоматическое обновление списка категорий при изменении типа (JS)
    class Media:
        js = ('js/admin_transaction.js',)
        
    def comment_preview(self, obj):
        """Ограничение длины комментария в списке"""
        return (obj.comment[:50] + '...') if obj.comment and len(obj.comment) > 50 else obj.comment or '-'
    comment_preview.short_description = 'Комментарий'
