# Generated by Django 5.1 on 2024-11-03 08:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('mystore', '0003_customer_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customer',
            name='password',
        ),
    ]