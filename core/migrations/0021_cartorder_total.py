# Generated by Django 4.2.8 on 2024-05-10 12:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0020_alter_cartorder_order_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='total',
            field=models.DecimalField(decimal_places=2, default='0.00', max_digits=12),
        ),
    ]
