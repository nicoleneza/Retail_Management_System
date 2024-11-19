from django import forms
from .models import Sale, SaleItem

class SaleForm(forms.ModelForm):
    customer_phone = forms.CharField(max_length=15, required=False, 
                                   help_text="Enter customer phone to use/earn points")
    use_points = forms.BooleanField(required=False)

    class Meta:
        model = Sale
        fields = ['payment_method', 'paid_amount']
        widgets = {
            'payment_method': forms.Select(attrs={'class': 'form-control'}),
            'paid_amount': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SaleItemForm(forms.ModelForm):
    class Meta:
        model = SaleItem
        fields = ['product', 'quantity']
        widgets = {
            'product': forms.Select(attrs={'class': 'form-control'}),
            'quantity': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
        }

SaleItemFormSet = forms.inlineformset_factory(
    Sale, SaleItem,
    form=SaleItemForm,
    extra=1,
    can_delete=True
) 