# Generated by Django 5.0 on 2024-02-25 15:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gz', '0024_alter_user_address_alter_user_city_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='state',
            field=models.CharField(max_length=20, null=True),
        ),
    ]