from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render
from django.contrib.auth import authenticate, login as django_login


def login(request):
    if request.user.is_authrnticated:
        if request.user.is_candidate:
            return HttpResponseRedirect(reverse('dashboard:candidate_home'))
        if request.user.is_company:
            return HttpResponseRedirect(reverse('dashboard:company_home'))
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
        if request.user.is_candidate:
            return HttpResponseRedirect(reverse('dashboard:candidate_home'))
        if request.user.is_company:
            return HttpResponseRedirect(reverse('dashboard:company_home'))
    else:
        return render(request, 'login.html')