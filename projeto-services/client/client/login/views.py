from django.http import HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login

from client.register.models import UserSession, Permission, Log, User


def login(request):
    if request.user.is_authenticated:
        if request.user.is_consumer:
            print('consumer')
        if request.user.is_company:
            print('company')
    else:
        if request.method == 'POST':
            return _login_method(request)
        else:
            return render(request, 'login.html')

def _login_method(request):
    username = request.POST['email']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        django_login(request, user)
        if request.user.is_consumer:
            print('consumer')
        if request.user.is_company:
            print('company')
    else:
        return render(request, 'login.html')