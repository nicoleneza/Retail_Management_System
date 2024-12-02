from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework import viewsets, permissions, status
from rest_framework.decorators import api_view, permission_classes
from sales.models import Sale
from .serializers import SaleSerializer
from django.db.models import Sum, Count, DecimalField
from django.db.models.functions import Coalesce, TruncDate, Cast
from django.utils import timezone
from datetime import timedelta
import logging
from django.db import connection

logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 500000  # Increased from 10
    page_size_query_param = 'page_size'
    max_page_size = 1000000  # Increased from 100


class SaleViewSet(viewsets.ModelViewSet):
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    pagination_class = StandardResultsSetPagination


@api_view(['GET'])
def sales_summary(request):
    try:
        with connection.cursor() as cursor:
            # Get total sales and revenue without date filter
            cursor.execute("""
                SELECT 
                    COUNT(*) as total_sales,
                    COALESCE(SUM(total_amount), 0) as total_revenue
                FROM sales_analytics
            """)
            
            totals = cursor.fetchone()
            total_sales = totals[0]
            total_revenue = float(totals[1])

            # Get daily sales breakdown
            cursor.execute("""
                SELECT 
                    DATE(date) as day,
                    COUNT(*) as sales,
                    COALESCE(SUM(total_amount), 0) as revenue,
                    customer_name,
                    invoice_number
                FROM sales_analytics
                GROUP BY DATE(date), customer_name, invoice_number
                ORDER BY day DESC
            """)
            
            columns = ['day', 'sales', 'revenue', 'customer', 'invoice_number']
            daily_sales = [dict(zip(columns, row)) for row in cursor.fetchall()]

        response_data = {
            'total_sales': total_sales,
            'total_revenue': total_revenue,
            'sales': daily_sales
        }
        
        return Response(response_data)

    except Exception as e:
        logger.error(f"Error in sales_summary: {str(e)}")
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def sales_customers(request):
    try:
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT 
                    invoice_number,
                    customer_name,
                    customer_address,
                    total_amount,
                    date,
                    payment_method
                FROM sales_analytics
                ORDER BY customer_name
            """)
            columns = [col[0] for col in cursor.description]
            customers = [dict(zip(columns, row)) for row in cursor.fetchall()]

        # Transform to match the CSV format
        customers_list = [{
            'Invoice Number': item['invoice_number'],
            'Customer Name': item['customer_name'],
            'Customer Address': item['customer_address'],
            'Total Amount': float(item['total_amount']),
            'Date': item['date'].strftime('%Y-%m-%d'),
            'Payment Method': item['payment_method']
        } for item in customers]

        # Apply pagination
        paginator = StandardResultsSetPagination()
        paginated_customers = paginator.paginate_queryset(customers_list, request)

        return paginator.get_paginated_response(paginated_customers)

    except Exception as e:
        logger.error(f"Error in sales_customers: {str(e)}")
        return Response({'error': str(e)}, status=500)


@api_view(['GET'])
def check_db(request):
    try:
        with connection.cursor() as cursor:
            # Check both tables
            cursor.execute("SELECT COUNT(*) FROM sales_analytics")
            sales_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM customers")
            customers_count = cursor.fetchone()[0]
            
            return Response({
                'sales_count': sales_count,
                'customers_count': customers_count
            })
    except Exception as e:
        logger.error(f"Database check error: {str(e)}")
        return Response({'error': str(e)}, status=500)
