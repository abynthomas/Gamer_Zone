# Generated by Django 5.0 on 2024-03-02 07:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0044_order_instruction'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='instruction',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='product_status',
            field=models.CharField(max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='purchase_date',
            field=models.DateTimeField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='status',
            field=models.CharField(max_length=20, null=True),
        ),
    ]
