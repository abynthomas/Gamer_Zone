# Generated by Django 5.0 on 2024-03-02 07:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0042_passwordreset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='date',
        ),
        migrations.AddField(
            model_name='order',
            name='delivery_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='order',
            name='purchase_date',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
