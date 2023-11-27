# Generated by Django 3.2.13 on 2023-11-24 10:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(blank=True, max_length=50, verbose_name='Имя пользователя')),
                ('password', models.TextField(blank=True, verbose_name='Пароль')),
                ('is_admin', models.BooleanField(blank=True, default=False, verbose_name='Является администратором')),
                ('profile_photo', models.ImageField(upload_to='', verbose_name='Фотография профиля')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ['username'],
            },
        ),
    ]
