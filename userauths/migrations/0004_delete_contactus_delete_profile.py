# Generated by Django 4.2.8 on 2024-04-30 15:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0003_alter_contactus_options_contactus_email_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='ContactUs',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]