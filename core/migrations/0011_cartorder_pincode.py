# Generated by Django 4.2.8 on 2024-04-27 09:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_cartorder_address_cartorder_city_cartorder_country_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='pincode',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
