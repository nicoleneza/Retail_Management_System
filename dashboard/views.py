from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from sales.models import Sale
from inventory.models import Product
from django.db.models import Sum, Count
from django.utils import timezone
from django.http import JsonResponse

def is_staff(user):
    return user.user_type == 'staff'

@login_required
@user_passes_test(is_staff)
def dashboard(request):
    # Get current month's data
    today = timezone.now()
    month_start = today.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    
    # Sales Statistics
    monthly_sales = Sale.objects.filter(
        date__gte=month_start,
        staff_member=request.user
    ).aggregate(
        total_amount=Sum('total_amount'),
        total_count=Count('id')
    )

    # Inventory Statistics
    low_stock_threshold = 10
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=low_stock_threshold
    ).count()

    context = {
        'total_sales': monthly_sales['total_amount'] or 0,
        'sales_count': monthly_sales['total_count'] or 0,
        'low_stock_products': low_stock_products,
        'recent_sales': Sale.objects.filter(staff_member=request.user).order_by('-date')[:5],
        'low_stock_items': Product.objects.filter(stock_quantity__lte=low_stock_threshold).order_by('stock_quantity')[:5],
    }
    
    return render(request, 'dashboard/index.html', context) 

def get_low_stock_count():
    low_stock_threshold = 10
    return Product.objects.filter(stock_quantity__lte=low_stock_threshold).count()

def calculate_total_sales():
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    sales = Sale.objects.filter(date__gte=month_start).aggregate(total=Sum('total_amount'))
    return sales['total'] or 0

def get_sales_count():
    month_start = timezone.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    return Sale.objects.filter(date__gte=month_start).count()

def get_recent_sales():
    return Sale.objects.order_by('-date')[:5].values()

def get_low_stock_items():
    low_stock_threshold = 10
    return Product.objects.filter(stock_quantity__lte=low_stock_threshold).order_by('stock_quantity')[:5].values()

@login_required
def dashboard_stats(request):
    # Get current stats
    stats = {
        'total_sales': calculate_total_sales(),
        'sales_count': get_sales_count(),
        'low_stock_products': get_low_stock_count(),
        'recent_sales': get_recent_sales(),
        'low_stock_items': get_low_stock_items()
    }
    return JsonResponse(stats) 