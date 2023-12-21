import os

from django.shortcuts import render, redirect
from django.core.files.base import ContentFile
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from copy import deepcopy
from .forms import *
from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
from operator import and_
from django.db.models import Q


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
        'admin_page': 'admin_page',
        'title': 'ARCHIVE'
    })


"""Функция регистрации пользователя"""


def register_page(request):
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

                response = redirect('home_page')
                #  сохранение имя текущего пользователя в куки-файле 
                response.set_cookie(key='username', value=form.cleaned_data['username'])

                return response
            #  введённый пароль не соответствует подтверждению
            else:
                form_error.error_is_raised = True
                form_error.error_message = 'Подтверждение пароля некорректно'

    #  переход на страницу без отправки формы
    return render(request, 'registration.html', context={
        'back_page': 'teaser_page',
        'form': RegistrationForm(None),
        'form_error': form_error,
        'title': 'Регистрация'
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
                response = redirect('home_page')
                #  сохранение имя текущего пользователя в куки-файле
                response.set_cookie(key='username', value=form.cleaned_data['username'])
                return response
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
        'form_error': form_error,
        'title': 'Регистрация'
    })


def home_page(request):
    """Домашняя страница пользователя"""

    return render(request, 'home.html', context={
        'person_page': 'profile_page',
        'back_page': 'teaser_page',
        'avatar': User.objects.values('profile_photo').get(username=request.COOKIES.get('username'))['profile_photo'],
        'add_file': 'add_file',
        'choose_tags': 'choose_tags',
        'title': 'Домашняя страница'
    })


def profile_page(request):
    """Страница личного кабинета"""

    #  получение информации о пользователе из базы данных
    #  с помощью имени пользователя из куки-файлов
    user = User.objects.values('username', 'password', 'email', 'profile_photo').get(
        username=request.COOKIES.get('username'))

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
        'avatar': user['profile_photo'],
        'title': 'Профиль'
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
                    User.objects.filter(username=request.COOKIES.get('username')).update(
                        username=form.cleaned_data['username'])
                    #  изменяем текущее имя пользователя в куки файле
                    response = redirect('profile_page')
                    response.set_cookie(key='username', value=form.cleaned_data['username'])
                    return response
            #  если редактируется пароль
            elif form_name == 'password_form':
                #  введённый старый пароль не совпадает с действующим паролем
                if user.password != form.cleaned_data['old_password']:
                    form_error.error_is_raised = True
                    form_error.error_message = 'Пароли не совпадают'
                else:
                    #  изменяем пароль и сохраняем
                    User.objects.filter(username=request.COOKIES.get('username')).update(
                        password=form.cleaned_data['password'])
                    return redirect('profile_page')
            #  если редактируется электронная почта
            elif form_name == 'email_form':
                #  изменяем адрес электронной почты и сохраняем и сохраняем
                User.objects.filter(username=request.COOKIES.get('username')).update(email=form.cleaned_data['email'])
                return redirect('profile_page')
            #  если редактируется фото профиля
            elif form_name == 'profile_photo_form':
                #  обновляем фотографию пользователя
                User.objects.filter(username=request.COOKIES.get('username')).update(
                    profile_photo=form.cleaned_data['photo'])
                #  сохраняем фотографию в дирректорию медийных файлов
                default_storage.save(f"profile/{form.cleaned_data['photo']}",
                                     ContentFile(request.FILES['photo'].read()))
                return redirect('profile_page')

    #  переход на страницу без отправки формы
    return render(request, 'edit_user.html', context={
        'form': request_forms[edit_id](None),
        'back_page': 'profile_page',
        'form_error': form_error,
        'title': 'Редактирование данных'
    })


def add_file(request):
    form_error = FormError()
    form_message = FormMessage()

    #  обработка запроса от формы
    if (request.method == 'POST'):
        form = AddFile(request.POST, request.FILES)
        if form.is_valid():
            # проверка на существаоние файла в бд
            if File.objects.all().filter(file_name=request.FILES['file'].name).exists():
                form_error.error_is_raised = True
                form_error.error_message = 'Файл с таким названием уже существует'
            else:
                # загрузка файла в хранилище на сервере
                file_in_storage = default_storage.save(request.FILES['file'].name, request.FILES['file'])
                # добавление файла в бд
                file = File(file_name=request.FILES['file'].name,
                            file_path=default_storage.url(file_in_storage),
                            file_size=request.FILES['file'].size)
                file.save()
                file.users.add(User.objects.all().get(username=request.COOKIES.get('username')))
                # добавление новых тэгов в бд и связь файла со всеми новыми тэгами
                # если пользователь создал новые тэги
                if not (len(form.cleaned_data['new_tags']) == 0):
                    for tag_name in form.cleaned_data['new_tags'].split(', '):
                        if not (Tag.objects.all().filter(tag_name=tag_name).exists()):
                            tag = Tag(tag_name=tag_name)
                            tag.save()
                            file.tags.add(tag)
                # связь файла с выбранными, существующими тэгами
                if (len(form.cleaned_data['existing_tags']) != 0):
                    for tag_id in form.cleaned_data['existing_tags']:
                        file.tags.add(Tag.objects.all().get(tag_id=tag_id))

                # сообщение для пользователя
                form_message.message_is_raised = True
                form_message.message = 'Файл успешно добавлен'

    return render(request, 'add_file.html', context={
        'back_page': 'home_page',
        'title': 'Добавление файла',
        'form': AddFile(None),
        'form_error': form_error,
        'form_message': form_message
    })


def choose_tags_page(request, flag):
    print(list([tag.tag_name for tag in Tag.objects.all()]))
    # работа со страницей, на которой выбираются тэги по которым будут искаться файлы
    form_error = FormError()
    form_tags = ChooseTags()
    # обработка запроса формы
    if (request.method == 'POST'):
        form = ChooseTags(request.POST)
        # пробел нужен, чтобы код работал, если пользователь не выбрал ни одного тэга
        tags = " "
        if form.is_valid():
            # если выбран хоть один тэг
            if (len(form.cleaned_data['existing_tags']) != 0):
                # создание строки с id всех выбранныз тэгов, для передачи следующей странице
                for tag_id in form.cleaned_data['existing_tags']:
                    tags += tag_id
                    tags += " "
            # функция выбора тэгов используется для удаления файлов и скачивания
            # если теги выбираются для установки файла flag = 0
            if (flag == 0):
                return HttpResponseRedirect(reverse('download_page', args=[tags]))
            # если для удаления файла flag = 1
            elif (flag == 1):
                return HttpResponseRedirect(reverse('delete_page', args=[tags, " "]))

    return render(request, 'choose_tags.html', context={
        'back_page': 'home_page',
        'title': 'Поиск по тэгам',
        'form': form_tags,
        'form_error': form_error,
        'button': "найти"
    })


def download_page(request, tags_id):
    # работа со страницей скачки файлов
    tags_id = list(map(int, tags_id.split()))
    files = File.objects.all()
    # нахождение всех файлов к которым пользователь имеет доступ
    files = files.filter(users__in=[(User.objects.all().get(username=request.COOKIES.get('username'))).pk])
    # если был выбран хоть один тэг, ищутся файлы содержащие все выбранные тэги
    # если не выбран ни один тэг, будут показаны все файлы пользователя
    if (len(tags_id) != 0):
        for tag in tags_id:
            files = files.filter(tags__in=[tag])
    return render(request, 'download_page.html', context={
        'back_page': 'choose_tags',
        'files': files
    })


def delete_page(request, tags_id, file_id):
    # работа со страницей даления файлов
    form_message = FormMessage()
    # строка из id тэгов нужна внутри файла для кнопок
    tags_id_str = deepcopy(tags_id)
    # если переход на страницу удаления произошел из-за нажатия кнопки "удалить" на странице удаления
    # то передан file_id удаляемого файла
    # если переход осуществлен со страницы с выбором тэгов file_id=" "
    if file_id != " ":
        File.objects.all().filter(pk=int(file_id)).delete()
        # отображение сообщения на странице об успешном удалении файла
        form_message.message_is_raised = True
        form_message.message = 'Файл успешно удален'
    # отображение сообщения на странице об успешном удалении файла
    tags_id = list(map(int, tags_id.split()))
    files = File.objects.all()
    # отображение всех оставшихся файлов
    # нахождение всех файлов к которым пользователь имеет доступ
    files = files.filter(users__in=[(User.objects.all().get(username=request.COOKIES.get('username'))).pk])
    # если был выбран хоть один тэг, ищутся файлы содержащие все выбранные тэги
    # если не выбран ни один тэг, будут фоказаны все файлы пользователя
    if (len(tags_id) != 0):
        for tag in tags_id:
            files = files.filter(tags__in=[tag])
    print("tags_id_str", tags_id_str)
    return render(request, 'delete_page.html', context={
        'back_page': 'choose_tags',
        'files': files,
        'tags_id_': tags_id_str,
        'form_message': form_message
    })


# обработка ошибок на сайте

def error_404(request, exception):
    # we add the path to the 404.html file
    return render(request, '404.html')


def error_500(request, exception):
    # we add the path to the 500.html file
    return render(request, '500.html')


def file_list(request):
    # Страница со списком файлов пользователя для дальнейшего редактирования тегов
    files = File.objects.all()
    return render(request, 'file_list.html', {'files': files})

def edit_file_tags(request, file_id):
    # Работа со страницей редактирования тегов
    form_error = FormError()
    form_message = FormMessage()
    file_instance = File.objects.get(pk=file_id)

    if request.method == 'POST':
        form = EditFileTagsForm(request.POST)
        if form.is_valid():
            # Существующие теги
            selected_tags = form.cleaned_data['existing_tags']
            file_instance.tags.clear()
            for tag_id in selected_tags:
                tag = Tag.objects.get(pk=tag_id)
                file_instance.tags.add(tag)
            # Новые теги
            new_tags_str = form.cleaned_data['new_tags']
            if new_tags_str:
                new_tags_list = [tag.strip() for tag in new_tags_str.split(',')]
                for tag_name in new_tags_list:
                    tag, created = Tag.objects.get_or_create(tag_name=tag_name)
                    file_instance.tags.add(tag)
            file_instance.save()
            form_message.message_is_raised = True
            form_message.message = 'Tags updated successfully.'
    else:
        # Если ввели слишком длинный новый тег - вносим только существующие
        current_tags = file_instance.tags.values_list('pk', flat=True)
        form = EditFileTagsForm(initial={'existing_tags': current_tags})
        form.fields['existing_tags'].choices = [(tag.pk, tag.tag_name) for tag in Tag.objects.all()]

    return render(request, 'edit_file_tags.html', {
        'form': form,
        'form_error': form_error,
        'form_message': form_message,
        'back_page': 'file_list'
    })
