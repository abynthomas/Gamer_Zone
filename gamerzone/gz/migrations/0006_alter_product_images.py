# Generated by Django 5.0 on 2024-01-18 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0005_images_remove_product_images_product_images'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='images',
            field=models.ManyToManyField(null=True, to='gz.images'),
        ),
    ]