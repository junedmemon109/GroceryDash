# Generated by Django 4.2.8 on 2024-05-02 14:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0019_cartorderitems_pid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cartorder',
            name='order_date',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='paid_status',
            field=models.CharField(choices=[('pending', 'Pending'), ('success', 'Success'), ('failure', 'Failure')], default='pending', max_length=30),
        ),
    ]