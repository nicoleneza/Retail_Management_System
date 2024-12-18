# Generated by Django 5.1.3 on 2024-11-19 04:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('inventory', '0001_initial'),
        ('sales', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RenameField(
            model_name='sale',
            old_name='created_at',
            new_name='date',
        ),
        migrations.RenameField(
            model_name='saleitem',
            old_name='total_price',
            new_name='price',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='balance',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='cashier',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='customer_name',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='sale_date',
        ),
        migrations.RemoveField(
            model_name='sale',
            name='updated_at',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='created_at',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='product_name',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='unit_price',
        ),
        migrations.RemoveField(
            model_name='saleitem',
            name='updated_at',
        ),
        migrations.AddField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(limit_choices_to={'user_type': 'customer'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='purchases', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='sale',
            name='points_earned',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sale',
            name='points_used',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='sale',
            name='staff_member',
            field=models.ForeignKey(limit_choices_to={'user_type': 'staff'}, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sales', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='saleitem',
            name='product',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='inventory.product'),
        ),
        migrations.AlterField(
            model_name='sale',
            name='invoice_number',
            field=models.CharField(max_length=20, unique=True),
        ),
        migrations.AlterField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(choices=[('cash', 'Cash'), ('card', 'Card'), ('mobile', 'Mobile Payment')], default='cash', max_length=10),
        ),
    ]
