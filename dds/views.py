from django.shortcuts import render, get_object_or_404, redirect
from rest_framework import viewsets
from .models import Transaction, Status, Type, Category, Subcategory
from .forms import TransactionForm
from django.db.models import Q
from datetime import date
from .serializers import TransactionSerializer

class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

def transaction_list(request):
    transactions = Transaction.objects.all().order_by('-created_at')

    # Фильтры
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    status_id = request.GET.get('status')
    type_id = request.GET.get('type')
    category_id = request.GET.get('category')
    subcategory_id = request.GET.get('subcategory')
    
    if start_date:
        transactions = transactions.filter(created_at__gte=start_date)
    if end_date:
        transactions = transactions.filter(created_at__lte=end_date)
    if status_id:
        transactions = transactions.filter(status_id=status_id)
    if type_id:
        transactions = transactions.filter(type_id=type_id)
    if category_id:
        transactions = transactions.filter(category_id=category_id)
    if subcategory_id:
        transactions = transactions.filter(subcategory_id=subcategory_id)

    # Если запрос был через HTMX — верни только таблицу
    if request.headers.get('HX-Request'):
        return render(request, 'partials/transaction_table.html', {'transactions': transactions})
    
    context = {
        'transactions': transactions,
        'statuses': Status.objects.all(),
        'types': Type.objects.all(),
        'categories': Category.objects.all(),
        'subcategories': Subcategory.objects.all(),
        'filters': request.GET,
    }
    return render(request, 'transaction_list.html', context)

def transaction_create(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm()
    return render(request, 'transaction_form.html', {'form': form})

def transaction_edit(request, pk):
    transaction = get_object_or_404(Transaction, pk=pk)
    if request.method == 'POST':
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('transaction_list')
    else:
        form = TransactionForm(instance=transaction)
    return render(request, 'transaction_form.html', {'form': form})

def transaction_delete(request, pk):
    obj = get_object_or_404(Transaction, pk=pk)
    obj.delete()
    return redirect('transaction_list')