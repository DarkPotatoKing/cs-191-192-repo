from django.shortcuts import render, redirect
from std.models import *
# Create your views here.
def index(request):
    #autheticated = False


    return render(request, 'std/login.html', {})

def login(request):
    return render(request, 'std/index.html', {})

def register(request):
    User.create(request.POST.get('uname'), request.POST.get('passw'))
    return render(request, 'std/index.html')