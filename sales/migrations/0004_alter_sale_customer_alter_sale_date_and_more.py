# Generated by Django 5.1.3 on 2024-11-25 07:54

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sales', '0003_customer_staffmember'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterField(
            model_name='sale',
            name='customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='customer_sales', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='sale',
            name='date',
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='payment_method',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='sale',
            name='points_earned',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='points_used',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='sale',
            name='staff_member',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='staff_sales', to=settings.AUTH_USER_MODEL),
        ),
    ]