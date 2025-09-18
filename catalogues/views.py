from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Status, Type, Category, Subcategory
from dds.models import Transaction
from .serializers import StatusSerializer, TypeSerializer, CategorySerializer, SubcategorySerializer
from .forms import (
    StatusForm,
    TypeForm,
    CategoryForm,
    SubcategoryForm
)

class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer

class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer

class SubcategoryViewSet(viewsets.ModelViewSet):
    queryset = Subcategory.objects.all()
    serializer_class = SubcategorySerializer
    
class CategoryListAPIView(APIView):
    """
    Возвращает список категорий, фильтруя по типу (через параметр ?type=)
    """
    def get(self, request):
        type_id = request.query_params.get('type')
        if not type_id:
            return Response([], status=200)  # пустой массив, если не указан тип

        try:
            categories = Category.objects.filter(type_id=type_id).order_by('name')
            serializer = CategorySerializer(categories, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response([], status=200)  # если type_id не число
    
class SubcategoryListAPIView(APIView):
    """
    Возвращает список подкатегорий, фильтруя по категории (через параметр ?category=)
    """
    def get(self, request):
        category_id = request.query_params.get('category')
        if not category_id:
            return Response([], status=200)

        try:
            subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name')
            serializer = SubcategorySerializer(subcategories, many=True)
            return Response(serializer.data)
        except ValueError:
            return Response([], status=200)
        
def catalogue_manage(request):
    # Все объекты
    statuses = Status.objects.all()
    types = Type.objects.all()
    categories = Category.objects.select_related('type').all()
    subcategories = Subcategory.objects.select_related('category__type').all()

    # Формы для создания
    status_form = StatusForm(request.POST or None, prefix='status')
    type_form = TypeForm(request.POST or None, prefix='type')
    category_form = CategoryForm(request.POST or None, prefix='category')
    subcategory_form = SubcategoryForm(request.POST or None, prefix='subcategory')

    if request.method == 'POST':
        if 'create_status' in request.POST and status_form.is_valid():
            status_form.save()
            messages.success(request, f"Статус '{status_form.instance.name}' добавлен.")
            return redirect('catalogue_manage')
        elif 'create_type' in request.POST and type_form.is_valid():
            type_form.save()
            messages.success(request, f"Тип '{type_form.instance.name}' добавлен.")
            return redirect('catalogue_manage')
        elif 'create_category' in request.POST and category_form.is_valid():
            category_form.save()
            messages.success(request, f"Категория '{category_form.instance.name}' добавлена.")
            return redirect('catalogue_manage')
        elif 'create_subcategory' in request.POST and subcategory_form.is_valid():
            subcategory_form.save()
            messages.success(request, f"Подкатегория '{subcategory_form.instance.name}' добавлена.")
            return redirect('catalogue_manage')
    
    context = {
        'statuses': statuses,
        'types': types,
        'categories': categories,
        'subcategories': subcategories,
        'status_form': status_form,
        'type_form': type_form,
        'category_form': category_form,
        'subcategory_form': subcategory_form,
        'messages': messages.get_messages(request),
    }
    return render(request, 'catalogue_manage.html', context)

def delete_status(request, pk):
    obj = get_object_or_404(Status, pk=pk)
    if Transaction.objects.filter(status=obj).exists():  # если используется
        messages.error(request, f"Нельзя удалить статус '{obj.name}', он используется в операциях.")
    else:
        obj.delete()
        messages.success(request, "Статус удалён.")
    return redirect('catalogue_manage')

def delete_type(request, pk):
    obj = get_object_or_404(Type, pk=pk)
    if Transaction.objects.filter(type=obj).exists() or Category.objects.filter(type=obj).exists():
        messages.error(request, f"Нельзя удалить тип '{obj.name}', он используется.")
    else:
        obj.delete()
        messages.success(request, "Тип удалён.")
    return redirect('catalogue_manage')

def delete_category(request, pk):
    obj = get_object_or_404(Category, pk=pk)
    if Transaction.objects.filter(category=obj).exists() or Subcategory.objects.filter(category=obj).exists():
        messages.error(request, f"Нельзя удалить категорию '{obj.name}', она используется.")
    else:
        obj.delete()
        messages.success(request, "Категория удалена.")
    return redirect('catalogue_manage')

def delete_subcategory(request, pk):
    obj = get_object_or_404(Subcategory, pk=pk)
    if Transaction.objects.filter(subcategory=obj).exists():
        messages.error(request, f"Нельзя удалить подкатегорию '{obj.name}', она используется.")
    else:
        obj.delete()
        messages.success(request, "Подкатегория удалена.")
    return redirect('catalogue_manage')

from django.shortcuts import render

def category_options(request):
    type_id = request.GET.get('type')
    categories = Category.objects.filter(type_id=type_id).order_by('name') if type_id else Category.objects.none()
    return render(request, 'partials/category_options.html', {'categories': categories})

def subcategory_options(request):
    category_id = request.GET.get('category')
    subcategories = Subcategory.objects.filter(category_id=category_id).order_by('name') if category_id else Subcategory.objects.none()
    return render(request, 'partials/subcategory_options.html', {'subcategories': subcategories})