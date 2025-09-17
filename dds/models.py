# dds/models.py
from django.db import models
from catalogues.models import Status, Type, Category, Subcategory

class Transaction(models.Model):
    created_at = models.DateField(auto_now_add=False, auto_now=False, default=models.functions.Now())
    # on_delete=models.PROTECT — чтобы нельзя было удалить используемый справочник. 
    status = models.ForeignKey(Status, on_delete=models.PROTECT)
    type = models.ForeignKey(Type, on_delete=models.PROTECT)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.PROTECT)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    comment = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.type.name}: {self.amount} руб. ({self.created_at})"