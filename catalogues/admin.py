from django.contrib import admin
from .models import Status, Type, Category, Subcategory

@admin.register(Status)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
    
@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'type')
    list_filter = ('type',)
    search_fields = ('name', 'type__name')
    ordering = ('type', 'name')
    
@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'type_via_category')
    list_filter = ('category', 'category__type') # фильтр по типу через категорию
    search_fields = ('name', 'category__name', 'category__type__name')
    ordering = ('category__type', 'category__name', 'name')
    
    def type_via_category(self, obj):
        return obj.category.type.name
    type_via_category.short_description = 'Тип'
    type_via_category.admin_order_field = 'category__type__name'  # сортировка по типу