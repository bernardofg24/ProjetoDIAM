from django.urls import include, path
from django.contrib import admin
from . import views
from django.conf import settings
from django.conf.urls.static import static

# (. significa que importa views da mesma directoria)

app_name = 'levelcheck'
urlpatterns = [
    path('', views.login_form, name='login_form'),
    path('logout', views.logout, name='logout'),
    path('createacc', views.create_acc, name='create_acc'),
    path('index', views.index, name='index'),
    path('profile/<str:username>', views.profile, name='profile'),
    path('editprofile/<int:id>', views.edit_profile, name='edit_profile'),
    path('creategame', views.create_game, name='create_game'),
    path('creategenre', views.create_genre, name='create_genre'),
    path('createcharacter', views.create_character, name='create_character'),
    path('allgames', views.all_games, name='all_games'),
    path('allcharacters', views.all_characters, name='all_characters'),
]
