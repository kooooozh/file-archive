from django.urls import path
from .views import *


urlpatterns = [
    path('', teaser_page, name='teaser_page'),
    path('registration/', register_page, name='registration_page'),
    path('entrance/', entrance_page, name='entrance_page'),
    path('home/', home_page, name='home_page'),
    path('home/profile/', profile_page, name='profile_page'),
    path('home/profile/<slug:edit_id>/', edit_user_info, name='edit_page'),
    path('home/add_file/', add_file, name='add_file')
]