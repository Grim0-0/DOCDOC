# Generated by Django 4.2.13 on 2024-05-21 10:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dcapp', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='document',
            name='image',
        ),
    ]