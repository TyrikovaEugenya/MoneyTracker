from django import forms
from .models import Status, Type, Category, Subcategory

class StatusForm(forms.ModelForm):
    class Meta:
        model = Status
        fields = ['name']
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Status.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Такой статус уже существует.")
        return name.title()

class TypeForm(forms.ModelForm):
    class Meta:
        model = Type
        fields = ['name']
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Type.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Такой тип уже существует.")
        return name.title()

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['name', 'type']
        

class SubcategoryForm(forms.ModelForm):
    class Meta:
        model = Subcategory
        fields = ['name', 'category']
        
    def clean_name(self):
        name = self.cleaned_data['name'].strip()
        if Status.objects.filter(name__iexact=name).exists():
            raise forms.ValidationError("Такой статус уже существует.")
        return name.title()