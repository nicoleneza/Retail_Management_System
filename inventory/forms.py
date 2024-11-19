from django import forms
from .models import Product, Category, Sale, SaleItem

class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'  # Or specify fields: ['name', 'price', etc.]

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