# Generated by Django 4.2.16 on 2024-12-09 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_user_is_bot_available'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_bot_available',
            field=models.BooleanField(default=False, verbose_name='Разрешить пользователю использовать бота'),
        ),
    ]
