# Generated by Django 5.0 on 2024-03-08 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0048_rename_status_order_payment_status_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='email',
        ),
    ]
