# Generated by Django 5.0 on 2024-02-25 16:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0026_product_company'),
    ]

    operations = [
        migrations.RenameField(
            model_name='product',
            old_name='company',
            new_name='product_key',
        ),
    ]