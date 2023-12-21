from django import forms
from .models import *


class FormError:
    """\
    Класс с флагом возбуждения ошибки формы и строкой сообщения
    <default> error_is_based : False
    <default> error_message : None
    """

    def __init__(self) -> None:
        #  флаг вызова ошибки при обработке запроса формы
        self.error_is_raised: bool = False
        #  строка сообщения ошибки
        self.error_message: str = None


class EnterForm(forms.Form):
    """Форма авторизации пользователя на сайте"""

    username = forms.SlugField(max_length=255, label="Имя пользователя",
                               required=True, widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        }))

    password = forms.SlugField(max_length=255, label="Пароль",
                               required=True, widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль',
        }))


class RegistrationForm(forms.Form):
    """Форма регистрации пользователя на сайте"""

    username = forms.SlugField(max_length=255, label="Имя пользователя",
                               required=True, widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        }))

    password = forms.SlugField(max_length=255, label="Пароль",
                               required=True, widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        }))

    confirm_password = forms.SlugField(max_length=255, label="Подтверждение пароля",
                                       required=True, widget=forms.PasswordInput(attrs={
            'placeholder': 'Повторно введите тот же пароль'
        }))

    email = forms.EmailField(label="Адрес электронной почты", required=True,
                             widget=forms.EmailInput(attrs={
                                 'placeholder': 'format@example.ru'
                             }))


class EditUsername(forms.Form):
    """Форма редактирования имени пользователя"""

    username = forms.SlugField(max_length=255, label="Новое имя пользователя",
                               required=True, widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        }))

    #  возврат имени формы для определения параметра редактирования
    def __str__(self) -> str:
        return 'username_form'


class EditPassword(forms.Form):
    """Форма редактирования пароля"""

    old_password = forms.SlugField(max_length=255, label="Старый пароль",
                                   required=True, widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите текущий пароль'
        }))

    new_password = forms.SlugField(max_length=255, label="Новый пароль",
                                   required=True, widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите новый пароль'
        }))

    #  возврат имени формы для определения параметра редактирования
    def __str__(self) -> str:
        return 'password_form'


class EditEmail(forms.Form):
    """Форма редактирования адреса электронной почты"""

    email = forms.EmailField(label="Новый адрес электронной почты почты",
                             required=True, widget=forms.EmailInput(attrs={
            'placeholder': 'format@example.ru'
        }))

    #  возврат имени формы для определения параметра редактирования
    def __str__(self) -> str:
        return 'email_form'


class EditProfilePhoto(forms.Form):
    """Форма редактирование аватара пользователя"""

    photo = forms.ImageField(label="Сменить фотографию профиля",
                             required=False)

    #  возврат имени формы для определения параметра редактирования
    def __str__(self) -> str:
        return 'profile_photo_form'


class FormMessage:
    """\
    Класс с флагом возбуждения сообщения формы и строкой сообщения
    неоюходимо, например, чтобы уведомить пользователя о успешном выполнении действия
    <default> message_is_based : False
    <default> message : None
    """

    def __init__(self) -> None:
        #  флаг вызова ошибки при обработке запроса формы
        self.message_is_raised: bool = False
        #  строка сообщения ошибки
        self.message: str = None


class AddFile(forms.Form):
    """форма для добавления нового файла"""
    # выбор тэгов среди уже существующих
    existing_tags = forms.MultipleChoiceField(label="Тэги",
                                              required=False, widget=forms.CheckboxSelectMultiple,
                                              choices=list([tag.pk, tag.tag_name] for tag in Tag.objects.all()))
    # строка для записи новых тэгов, относащихся к файлу
    new_tags = forms.CharField(required=False, max_length=255, label="Новые тэги", widget=forms.TextInput(attrs={
        'placeholder': 'Введите через запятую новые тэги'
    }))
    # поле для загрузки файла
    file = forms.FileField(label="Выберите файл",
                           required=True, widget=forms.ClearableFileInput)


class ChooseTags(forms.Form):
    '''форма для выбора тэгов по которым будет искаться файл'''

    existing_tags = forms.MultipleChoiceField(label="Выберите тэги",
                                              required=False, widget=forms.CheckboxSelectMultiple,
                                              choices=list([tag.tag_id, tag.tag_name] for tag in Tag.objects.all()))


class EditFileTagsForm(forms.Form):
    '''Форма для редактирования тегов'''
    existing_tags = forms.MultipleChoiceField(
        label="Tags",
        required=False,
        widget=forms.CheckboxSelectMultiple,
        choices=list((tag.pk, tag.tag_name) for tag in Tag.objects.all())
    )
    new_tags = forms.CharField(
        required=False,
        max_length=100,
        label="New tags",
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите новые теги через запятую и пробел'
        })
    )