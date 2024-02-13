
from django.urls import path,include

from app.views import *

urlpatterns = [
    path('',home, name='home'),
    path('create/',create,name='create'),
    path('managefood/',managefood,name='managefood'),
    path('managefood/<str:date>/',managefood,name='managefood_add'),
    path('select_date/',select_date,name='select_date'),
    path('history_sale/',select_date,name='select_date'),
    path('clear_food/',clearfood,name='clear_food'),
    path('updatefood/<int:id>/',updatefood,name='updatefood'),
    path('search/',search,name='search'),
    path('review/<int:id>/',reviewfood,name='review'),
    path('admin1/', admin1, name='admin1'),
    path('management/', admin1, name='management'),
    path('profile/', profile, name='profile'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('me/', Me, name='me'),
    path('login/',login,name='custom_login'),
    path('line-login/', line_login, name='line'),
    path('login/callback/',line_callback,name='line_ callback'),
] 
