from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.db import transaction
from .models import Sale, SaleItem
from .forms import SaleForm, SaleItemFormSet
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
import pandas as pd
from django.http import HttpResponse
from datetime import datetime

User = get_user_model()

def is_staff(user):
    return user.user_type == 'staff'

@login_required
@user_passes_test(is_staff)
def create_sale(request):
    if not request.user.user_type == 'staff':
        messages.error(request, "Only staff members can create sales.")
        return redirect('sales:index')
    
    if request.method == 'POST':
        sale_form = SaleForm(request.POST)
        
        if sale_form.is_valid():
            sale = sale_form.save(commit=False)
            sale.staff_member = request.user
            
            customer_username = request.POST.get('customer_username')
            if customer_username:
                try:
                    customer = User.objects.get(username=customer_username)
                    sale.customer = customer
                except User.DoesNotExist:
                    messages.warning(request, "Customer not found.")
                  
            # Generate invoice number
            last_sale = Sale.objects.order_by('-id').first()
            sale.invoice_number = f"INV{(last_sale.id + 1 if last_sale else 1):06d}"
            
            sale.save()
          
            if sale.customer:
                points_earned = int(sale.total_amount * 10)
                sale.customer.points += points_earned
                sale.customer.save()
                messages.success(request, f"Sale created successfully. {points_earned} points earned.")
        
            messages.success(request, 'Sales recorded successfully.')
            return redirect('sales:index')
    else:
        sale_form = SaleForm()
    return render(request, 'sales/create_sale.html', {'form': sale_form})

@login_required
def check_customer(request, username):
    try:
        customer = User.objects.get(username=username, user_type='customer')
        return JsonResponse({
            'success': True,
            'customer': {
                'username': customer.username,
                'name': customer.get_full_name() or customer.username,
                'points': customer.points
            }
        })
    except User.DoesNotExist:
        return JsonResponse({
            'success': False,
            'message': 'Customer not found'
        })

class SaleListView(LoginRequiredMixin, ListView):
    model = Sale
    template_name = 'sales/sale_list.html'
    context_object_name = 'sales'
    ordering = ['-date']

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.user_type == 'staff':
            return queryset.filter(staff_member=self.request.user)
        elif self.request.user.user_type == 'customer':
            return queryset.filter(customer=self.request.user)
        return Sale.objects.none()
    
    def get(self, request, *args, **kwargs):
        if 'export' in request.GET:
            sales = self.get_queryset()
            data = []
            for sale in sales:
                data.append({
                    'Invoice Number': sale.invoice_number,
                    'Date': sale.date,
                    'Customer': sale.customer.username if sale.customer else 'Anonymous',
                    'Total Amount': sale.total_amount,
                    'Points Earned': sale.points_earned,
                })
            df = pd.DataFrame(data)

            if request.GET['export'] == 'excel':
                response = HttpResponse(content_type='application/vnd.ms-excel')
                response['Content-Disposition'] = f'attachment; filename=sales_{datetime.now().strftime("%Y%m%d")}.xlsx'
                df.to_excel(response, index=False)
                return response
            
            elif request.GET['export'] == 'csv':
                response = HttpResponse(content_type='text/csv')
                response['Content-Disposition'] = f'attachment; filename=sales_{datetime.now().strftime("%Y%m%d")}.csv'
                df.to_csv(response, index=False)
                return response
        
        return super().get(request, *args, **kwargs)

@login_required
def sale_detail(request, pk):
    sale = get_object_or_404(Sale, pk=pk)
    if request.user.user_type == 'customer' and sale.customer != request.user:
        messages.error(request, "You are not authorized to view this sale.")
        return redirect('sales:index')
    return render(request, 'sales/sale_detail.html', {'sale': sale})

class CustomerPurchaseHistory(LoginRequiredMixin, ListView):
    template_name = 'sales/customer_history.html'
    context_object_name = 'purchases'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.user_type != 'customer':
            return Sale.objects.none()
        return Sale.objects.filter(
            customer=self.request.user
        ).order_by('-date')
