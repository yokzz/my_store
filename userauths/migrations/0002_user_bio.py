# Generated by Django 5.0.7 on 2024-07-14 22:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='bio',
            field=models.CharField(default=1, max_length=63),
            preserve_default=False,
        ),
    ]
