# Generated by Django 5.0 on 2024-02-28 17:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0036_rename_first_name_order_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='order',
            old_name='product',
            new_name='product_order',
        ),
    ]
