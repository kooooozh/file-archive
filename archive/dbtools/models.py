from django.db import models


class User(models.Model):
    """\
    Таблица пользователей в базе данных.
    Атрибуты таблицы:

    ---------------------------------------
    | username | password | email | photo |
    ---------------------------------------
    |               /записи/              |
    ---------------------------------------
    """

    username = models.CharField(primary_key=True, max_length=50, 
                                verbose_name='Имя пользователя',
                                blank=False, null=False)

    password = models.TextField(verbose_name='Пароль', blank=False, null=False)

    email = models.EmailField(verbose_name='Адрес электронной почты',
                              blank=False, null=True)

    profile_photo = models.ImageField(upload_to='media/profile/', 
                                      verbose_name='Фотография профиля',
                                      blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']
