# Generated by Django 4.2.8 on 2024-04-27 16:58

from django.db import migrations
import shortuuid.django_fields


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0011_cartorder_pincode'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartorder',
            name='oid',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=20, null=True, prefix='SKU'),
        ),
        migrations.AlterField(
            model_name='cartorder',
            name='sku',
            field=shortuuid.django_fields.ShortUUIDField(alphabet='1234567890', blank=True, length=5, max_length=20, null=True, prefix='SKU'),
        ),
    ]