from django.conf import settings

import os
from django.shortcuts import render, redirect
import datetime
from .models import *
import requests
from django.contrib.auth import authenticate, login as auth_login,logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.db.models.fields.related import ManyToManyField
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.http import HttpResponse,Http404
def home(request):
    return render(request,'category_page/index.html')


