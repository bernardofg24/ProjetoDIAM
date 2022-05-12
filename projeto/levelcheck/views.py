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

# Create your views here.
