from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
        
    def validate(self, data):
        transaction_type = data.get('type')
        transaction_category = data.get('category')
        transaction_subcategory = data.get('subcategory')
        
        # Проверка: категория должна быть привязана к типу
        if transaction_category and transaction_type and transaction_category.type != transaction_type:
            raise serializers.ValidationError({
                "category": f"Категория '{transaction_category.name}' не относится к типу '{transaction_type.name}'."
            })
        
        # Проверка: подкатегория должна быть привязана к категории
        if transaction_subcategory and transaction_category and transaction_subcategory.category != transaction_category:
            raise serializers.ValidationError({
                "subcategory": f"Подкатегория '{transaction_subcategory.name}' не относится к категории '{transaction_category.name}'."
            })

        return data