# Generated by Django 5.0.7 on 2024-09-14 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0004_profile_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='ContactUs',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=63)),
                ('email', models.EmailField(max_length=254)),
                ('last_name', models.CharField(max_length=63)),
                ('phone', models.CharField(max_length=63)),
                ('subject', models.CharField(max_length=127)),
                ('message', models.TextField()),
            ],
        ),
    ]
