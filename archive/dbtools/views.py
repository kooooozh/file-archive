from django.shortcuts import render, redirect
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import HttpResponse
from .forms import *


def teaser_page(request):
    """Функция тизерной страницы"""
    
    #  куки-файлы уже содержат имя пользователя 
    #  (пользователь уже зарегестрирован, выполняеся выход из аккаунта)
    if request.COOKIES.get('username') is not None:
        #  перенаправление на страницу входа или регистрации
        response = redirect('teaser_page')
        #  удаление имени пользователя из куки-файда (выход из аккаунта)
        response.delete_cookie('username')
        return response

    return render(request, 'teaser.html', context={
        'enter_page': 'entrance_page',
        'register_page': 'registration_page',
        'admin_page': 'admin_page'
    })


def register_page(request):
    """Функция регистрации пользователя"""

    form_error = FormError()

    #  обработка запроса от формы
    if (request.method == 'POST'):
        form = RegistrationForm(request.POST)

        if form.is_valid():
            #  пользователь с указанным именем уже зарегестрирован в системе
            if User.objects.all().filter(username=form.cleaned_data['username']).exists():
                form_error.error_is_raised = True
                form_error.error_message = 'Пользователь с таким именем уже существует'
            #  проверка соотвестсвия введённого пароля и его подтверждения
            elif form.cleaned_data['password'] == form.cleaned_data['confirm_password']:
                #  создание и сохранение нового пользователя
                #  в базе данных при успешной проверке
                user = User(username=form.cleaned_data['username'],
                          password=form.cleaned_data['password'],
                          email=form.cleaned_data['email'])
                user.save()

                resopnse = redirect('home_page')
                #  сохранение имя текущего пользователя в куки-файле 
                resopnse.set_cookie(key='username', value=form.cleaned_data['username'])

                return resopnse
            #  введённый пароль не соответствует подтверждению
            else:
                form_error.error_is_raised = True
                form_error.error_message = 'Подтверждение пароля некорректно'
    
    #  переход на страницу без отправки формы
    return render(request, 'registration.html', context={
        'back_page': 'teaser_page',
        'form': RegistrationForm(None),
        'form_error': form_error
    })


def entrance_page(request):
    """Функция авторизации пользователя"""

    form_error = FormError()

    #  обработка запроса от формы
    if (request.method == 'POST'):
        form = EnterForm(request.POST)

        if form.is_valid():
            #  пользователь с указанным логином и паролем существует в базе данных
            if User.objects.all().filter(username=form.cleaned_data['username'],
                                         password=form.cleaned_data['password']).exists():
                resopnse = redirect('home_page')
                #  сохранение имя текущего пользователя в куки-файле
                resopnse.set_cookie(key='username', value=form.cleaned_data['username'])
                return resopnse
            #  возникла ошибка при поиске пользователя в базе данных
            else:
                form_error.error_is_raised = True

                if User.objects.all().filter(username=form.cleaned_data['username']).exists() == False:
                    form_error.error_message = 'Не существует пользователя с указанным именем'
                else:
                    form_error.error_message = 'Пароль указан неверно'

    #  переход на страницу без отправки формы
    return render(request, 'entrance.html', context={
        'back_page': 'teaser_page',
        'form': EnterForm(None),
        'form_error': form_error
    })


def home_page(request):
    """Домашняя страница пользователя"""

    return render(request, 'home.html', context={
        'person_page': 'profile_page',
        'back_page': 'teaser_page',
        'avatar': User.objects.values('profile_photo').get(username=request.COOKIES.get('username'))['profile_photo']
    })


def profile_page(request):
    """Страница личного кабинета"""

    #  получение информации о пользователе из базы данных
    #  с помощью имени пользователя из куки-файлов
    user = User.objects.values('username', 'password', 'email', 'profile_photo').get(username=request.COOKIES.get('username'))

    return render(request, 'profile.html', context={
        'username': user['username'],
        'password': "*" * len(user['password']),
        'email': user['email'],
        'back_page': 'home_page',
        'teaser_page': 'teaser_page',
        'edit_page': 'edit_page',
        'username_edit': 'username_edit',
        'email_edit': 'email_edit',
        'password_edit': 'password_edit',
        'photo_edit': 'profile_photo_edit',
        'avatar': user['profile_photo']
    })


def edit_user_info(request, edit_id):
    """\
    Страница редактирования данных. edit_id - параметр редактирования, указывающий,
    какие данные пользователь желает изменить
    """

    form_error = FormError()
    #  список параметров редактирования
    request_forms = {
        'username_edit': EditUsername,
        'password_edit': EditPassword,
        'email_edit': EditEmail,
        'profile_photo_edit': EditProfilePhoto
    }

    #  обработка запроса от формы
    if (request.method == 'POST'):
        #  создание объекта формы с информацией из формы страницы
        #  в зависимости от параметра редактирования
        form = request_forms[edit_id](request.POST, request.FILES)
        if form.is_valid():
            #  получение информации о текущем пользователе из базы данных
            #  с помощью имени пользователя из куки-файлов
            user = User.objects.get(username=request.COOKIES.get('username'))
            #  получение имени формы, указывающее редактируемый параметр
            form_name = str(form)
            #  если редактируется имя пользователя
            if form_name == 'username_form':
                #  пользователь с введённым именем уже существует
                if User.objects.all().filter(username=form.cleaned_data['username']).exists():
                    form_error.error_is_raised = True
                    form_error.error_message = 'Пользователь с введённым именем уже существует'
                else:
                    #  сохраняем новое имя пользователя
                    User.objects.filter(username=request.COOKIES.get('username')).update(username=form.cleaned_data['username'])
                    #  изменяем текущее имя пользователя в куки файле
                    resopnse = redirect('profile_page')
                    resopnse.set_cookie(key='username', value=form.cleaned_data['username'])
                    return resopnse
            #  если редактируется пароль
            elif form_name == 'password_form':
                #  введённый старый пароль не совпадает с действующим паролем
                if user.password != form.cleaned_data['old_password']:
                    form_error.error_is_raised = True
                    form_error.error_message = 'Пароли не совпадают'
                else:
                    #  изменяем пароль и сохраняем
                    User.objects.filter(username=request.COOKIES.get('username')).update(password=form.cleaned_data['password'])
                    return redirect('profile_page')
            #  если редактируется электронная почта
            elif form_name == 'email_form':
                #  изменяем адрес электронной почты и сохраняем и сохраняем
                User.objects.filter(username=request.COOKIES.get('username')).update(email=form.cleaned_data['email'])
                return redirect('profile_page')
            #  если редактируется фото профиля
            elif form_name == 'profile_photo_form':
                #  обновляем фотографию пользователя
                User.objects.filter(username=request.COOKIES.get('username')).update(profile_photo=form.cleaned_data['photo'])
                #  сохраняем фотографию в дирректорию медийных файлов
                default_storage.save(f"profile/{form.cleaned_data['photo']}", ContentFile(request.FILES['photo'].read()))
                return redirect('profile_page')
    
    #  переход на страницу без отправки формы
    return render(request, 'edit_user.html', context={
        'form': request_forms[edit_id](None),
        'back_page': 'profile_page',
        'form_error': form_error
    })