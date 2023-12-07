from django.urls import path
from .views import *
from django.urls import re_path
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve

urlpatterns = [
    path('', teaser_page, name='teaser_page'),
    path('registration/', register_page, name='registration_page'),
    path('entrance/', entrance_page, name='entrance_page'),
    path('home/', home_page, name='home_page'),
    path('home/profile/', profile_page, name='profile_page'),
    path('home/profile/<slug:edit_id>/', edit_user_info, name='edit_page'),
    path('home/add_file/', add_file, name='add_file'),
    path('home/download_<tags_id>/', download_page, name='download_page'),
    path('home/choose_tags/<int:flag>/', choose_tags_page, name="choose_tags"),
    path('home/delete/<tags_id>/<file_id>/', delete_page, name='delete_page')
]
