from django import forms
from .models import Product, Category, Sale, SaleItem

class ProductForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        empty_label="Select a category",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': 'required'
        })
    )
    
    class Meta:
        model = Product
        fields = ['name', 'category', 'sku', 'description', 'price', 'stock_quantity', 'reorder_level']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'sku': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'price': forms.NumberInput(attrs={'class': 'form-control'}),
            'stock_quantity': forms.NumberInput(attrs={'class': 'form-control'}),
            'reorder_level': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = '__all__' 

class SaleForm(forms.ModelForm):
    class Meta:
        model = Sale
        fields = ['customer','total_amount']  # adjust fields based on your Sale model

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity', 'price']  # adjust fields based on your SaleItem model

SaleItemFormSet = forms.inlineformset_factory(
    Sale, 
    SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True
) 