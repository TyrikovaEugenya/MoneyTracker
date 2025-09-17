from django.contrib import admin
from .models import Transaction

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
