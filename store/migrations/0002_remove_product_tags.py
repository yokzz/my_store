# Generated by Django 5.0.7 on 2024-07-24 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='tags',
        ),
    ]
