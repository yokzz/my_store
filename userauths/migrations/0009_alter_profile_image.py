# Generated by Django 5.0.7 on 2024-09-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('userauths', '0008_alter_profile_image'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='static/default_profile_picture.jpg', upload_to='profile_picture'),
        ),
    ]
