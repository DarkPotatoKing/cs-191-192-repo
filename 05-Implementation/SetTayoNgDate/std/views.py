from django.shortcuts import render, redirect
from std.models import *
# Create your views here.
def index(request):
    #autheticated = False


    return render(request, 'std/login.html', {})

def login(request):
    #request.POST.get('uname'), request.POST.get('passw') user and password input
    #insert the function here
    #if successful, return index
    #else, return to login page with error
    error = not (User.authenticate(request.POST.get('uname'), request.POST.get('passw')))
    if error:
        return render(request, 'std/login.html', {"fail": True})
    else:
        return render(request, 'std/home.html')


def register(request):
    User.create(request.POST.get('uname'), request.POST.get('passw'))
    return render(request, 'std/index.html')

def home(request):
    return render(request, 'std/home.html')