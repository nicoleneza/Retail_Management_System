from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet
from accounts.models import UserProfile
from inventory.models import Product
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

User = get_user_model()

def is_staff(user):
    return user.user_type == 'staff'

@login_required
@user_passes_test(is_staff)  # Only staff can access this view
def create_sale(request):
    if not request.user.user_type == 'staff':
        messages.error(request, "Only staff members can create sales.")
        return redirect('sales:index')
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.staff_member = request.user
            
            # Generate invoice number
            last_sale = Sale.objects.order_by('-id').first()
            sale.invoice_number = f"INV{(last_sale.id + 1 if last_sale else 1):06d}"
            
            sale.save()
            return redirect('sales:index')
    else:
        sale_form = SaleForm()
    return render(request, 'sales/create_sale.html', {'form': sale_form})

@login_required
def check_customer(request, phone):
    try:
        customer = UserProfile.objects.get(phone=phone, user_type='customer')
        return JsonResponse({
            'customer': {
                'name': customer.user.get_full_name() or customer.user.username,
                'points': customer.points
            }
        })
    except UserProfile.DoesNotExist:
        return JsonResponse({'customer': None})

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.userprofile.user_type == 'staff':
            return queryset.filter(staff_member=self.request.user)
        return queryset
    
@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.user.user_type == 'customer' and sale.customer != request.user:
        messages.error(request, "You are not authorized to view this sale.")
        return redirect('sales:index')
    return render(request, 'sales/sale_detail.html',{'sale':sale})
