# Generated by Django 4.2.8 on 2024-05-01 09:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0017_delete_profile'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='cart_status',
            field=models.BooleanField(default=True),
        ),
    ]