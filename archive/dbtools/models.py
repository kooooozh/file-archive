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

    # Механизм связывания пользователя с группами
    # blank=True, т.к. пользователь может не состоять ни в одной группе
    groups = models.ManyToManyField('Group', blank=True, related_name='groups')

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ['username']


class Group(models.Model):
    """\
    Таблица с именами групп
    Атрибуты таблицы:
    -------------------------
    | group_id | group_name |
    -------------------------
    |        /Записи/       |
    -------------------------
    """
    group_id = models.AutoField(primary_key=True, verbose_name='Id группы',
                                blank=False, null=False)

    group_name = models.CharField(verbose_name='Имя группы', max_length=100,
                                  blank=False, null=False)

    def __str__(self):
        return self.group_name

    class Meta:
        verbose_name = 'Группа'
        verbose_name_plural = 'Группы'
        ordering = ['group_name']


class File(models.Model):
    """\
    Таблица с данными о файле в базе данных
    Атрибуты таблицы:
    --------------------------------------------------------------
    |file_id|file_name|file_size|file_path|time_create|time_update|
    ---------------------------------------------------------------
    |                          /Записи/                           |
    ---------------------------------------------------------------
    """

    file_id = models.AutoField(primary_key=True, verbose_name='Id файла')

    file_name = models.CharField(verbose_name='Имя файла', max_length=255)

    file_size = models.IntegerField(verbose_name='Размер файла')

    file_path = models.CharField(verbose_name='Путь до файла', max_length=255)

    time_create = models.DateTimeField(verbose_name='Дата создания', auto_now_add=True)

    time_update = models.DateTimeField(verbose_name='Последнее изменение', auto_now=True)

    # Механизм связывания файлов с тегами, blank=True, т.к. некоторые файлы могут не иметь тегов
    tags = models.ManyToManyField('Tag', blank=True, related_name='tags')

    # Механизм связывания файлов с пользователями,
    # blank=False, т.к. в базе данных не должно быть "бесхозных" файлов
    users = models.ManyToManyField('User', blank=False, related_name='users')

    def __str__(self):
        return self.file_name

    class Meta:
        verbose_name = 'Файл'
        verbose_name_plural = 'Файлы'
        ordering = ['file_name']


class Tag(models.Model):
    """\
    Таблица с названиями тегов
        Атрибуты таблицы:
    -------------------------
    |   tag_id | tag_name   |
    -------------------------
    |        /Записи/       |
    -------------------------
    """
    tag_id = models.AutoField(primary_key=True, verbose_name='Id группы',
                              blank=False, null=False)

    tag_name = models.CharField(verbose_name='Имя группы', max_length=100,
                                blank=False, null=False)

    def __str__(self):
        return self.tag_name

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ['tag_name']
