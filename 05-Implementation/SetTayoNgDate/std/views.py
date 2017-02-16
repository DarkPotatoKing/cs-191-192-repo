"""
Copyright 2017 Manifold Cheddar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is a course requirement for CS 192 Software Engineering II under the supervision of Asst. Prof. Ma. Rowena C. Solamo of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman for the AY 2016-2017.

"""
#2/10/17 - Edward James Bariring - finished doing basic views; more to be added
#2/16/17 - Edward James Bariring - added methods for authentication

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
    #to do: add error detection for user creation
    User.create(request.POST.get('uname'), request.POST.get('passw'))
    return render(request, 'std/index.html')

def home(request):
    return render(request, 'std/home.html')
