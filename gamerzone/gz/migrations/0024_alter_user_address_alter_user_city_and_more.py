# Generated by Django 5.0 on 2024-02-24 10:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0023_user_address_user_city_user_country_user_zipcode_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='address',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='city',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='country',
            field=models.CharField(max_length=15, null=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='zipcode',
            field=models.CharField(max_length=10, null=True),
        ),
    ]
