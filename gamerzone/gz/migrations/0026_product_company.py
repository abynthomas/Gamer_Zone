# Generated by Django 5.0 on 2024-02-25 16:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0025_user_state'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='company',
            field=models.CharField(max_length=10, null=True),
        ),
    ]