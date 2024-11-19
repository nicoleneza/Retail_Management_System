from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from django.core.wsgi import get_wsgi_application
import django
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project_name.settings')
django.setup()

from sales.models import Sale
from inventory.models import Product

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/sales/stats")
async def get_sales_stats():
    total_sales = Sale.objects.count()
    total_products = Product.objects.count()
    return {
        "total_sales": total_sales,
        "total_products": total_products
    }

@app.get("/api/products/low-stock")
async def get_low_stock():
    low_stock_products = Product.objects.filter(
        stock_quantity__lte=models.F('reorder_level')
    ).values('id', 'name', 'stock_quantity', 'reorder_level')
    return list(low_stock_products)