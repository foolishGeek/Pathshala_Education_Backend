# Generated by Django 3.0.3 on 2020-02-18 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('campus_registration', '0004_auto_20200218_1823'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campusregistration',
            name='coordinator_name',
            field=models.CharField(default='', max_length=64),
        ),
    ]