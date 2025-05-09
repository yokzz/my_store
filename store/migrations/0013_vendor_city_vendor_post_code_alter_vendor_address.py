# Generated by Django 5.0.7 on 2024-07-30 15:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_address_post_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='vendor',
            name='city',
            field=models.CharField(blank=True, max_length=63, null=True),
        ),
        migrations.AddField(
            model_name='vendor',
            name='post_code',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='vendor',
            name='address',
            field=models.CharField(max_length=127, null=True),
        ),
    ]
