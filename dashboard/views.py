from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Sum, Count
from django.utils import timezone
from datetime import timedelta
from inventory import models
from sales.models import Sale
from inventory.models import Product
from orders.models import PurchaseOrder

class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'dashboard/index.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        today = timezone.now()
        thirty_days_ago = today - timedelta(days=30)
        
        # Sales statistics
        context['total_sales'] = Sale.objects.filter(
            sale_date__gte=thirty_days_ago
        ).aggregate(total=Sum('total_amount'))['total'] or 0
        
        # Inventory statistics
        context['low_stock_products'] = Product.objects.filter(
            stock_quantity__lte=models.F('reorder_level')
        ).count()
        
        # Orders statistics
        context['pending_orders'] = PurchaseOrder.objects.filter(
            status='pending'
        ).count()
        
        return context 