from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from django.urls import reverse
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.contrib.auth import authenticate, login, logout as django_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required, permission_required
from .models import *


def login_form(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            if not request.user.is_authenticated:
                login(request, user)
                return HttpResponseRedirect('index')
            else:
                return render(request, 'levelcheck/login_form.html', {'err_dupe': "You're already logged in."})
        else:
            return render(request, 'levelcheck/login_form.html', {'err_creds': "Username or Password are incorrect."})
        return
    else:
        return render(request, 'levelcheck/login_form.html')


@login_required(login_url='/levelcheck')
def logout(request):
    django_logout(request)
    return HttpResponseRedirect('/levelcheck')


def create_acc(request):
    if request.method == 'POST':
        username = request.POST['username']

        if User.objects.filter(username=username).exists():
            return render(request, 'levelcheck/create_acc.html', {'err_username': "Username in use."})
        email = request.POST['email']
        if User.objects.filter(email=email).exists():
            return render(request, 'levelcheck/create_acc.html', {'err_email': "E-mail in use."})

        email = request.POST['email']
        password = request.POST['password']
        birthday = request.POST['birthday']
        src = "projeto/levelcheck/static/website/images/jiggly.jpg"
        joined = timezone.now()

        u = User.objects.create_user(username, email, password)
        u.save()
        level = LevelUser(user=u, birthday=birthday, img_src=src, joined=joined)
        level.save()
        stats = UserStats(leveluser=level)
        stats.save()
        return HttpResponseRedirect(reverse('levelcheck:login_form'))
    else:
        return render(request, 'levelcheck/create_acc.html')


@login_required(login_url='/levelcheck')
def index(request):
    return render(request, 'levelcheck/index.html')


@login_required(login_url='/levelcheck')
def profile(request):
    return render(request, 'levelcheck/profile.html')
