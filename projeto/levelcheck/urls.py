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
]
