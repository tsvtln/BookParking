# Generated by Django 5.1.4 on 2024-12-30 00:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('booker', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='account',
            name='first_name',
            field=models.CharField(max_length=30),
        ),
        migrations.AlterField(
            model_name='account',
            name='second_name',
            field=models.CharField(max_length=30),
        ),
    ]