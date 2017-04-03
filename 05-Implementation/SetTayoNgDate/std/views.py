"""
Copyright 2017 Manifold Cheddar

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

This is a course requirement for CS 192 Software Engineering II under the supervision of Asst. Prof. Ma. Rowena C. Solamo of the Department of Computer Science, College of Engineering, University of the Philippines, Diliman for the AY 2016-2017.

"""
#2/10/17 - Edward James Bariring - finished doing basic views; more to be added
#2/16/17 - Edward James Bariring - added methods for authentication

"""TODO: #arvin, select mo nalang ung user ID using uID tapos sa schedule all gamitin mo ung uID para malaman if alin ididisplay
    tapos same lang sa edit profile and stuff, basta pagkuha nung data pasa mo nalang as parameter ung userID.

    sa editprofile pag dating ng post palagay nung user ID sa data na isusubmit, same lang sa ibang functions.
    di ako sure kung makukuha nya kasi ung user ID :DDD
"""

from django.shortcuts import render, redirect
from std.models import *


# Create your views here.
def index(request):
    #autheticated = False
    if 'curr_ID' in request.session:
        return redirect(profile)
    else:
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
        currentUser = User.objects.get(username=request.POST.get('uname'))
        request.session['curr_ID'] = currentUser.id
        return redirect(profile)

def profile(request):
    #checks if user is logged in, if not return to login screen
    try:
        curr_ID = request.session['curr_ID']
    except:
        return redirect(index)
    #replace schedule all with a string of scheds (same as saveprofile)
    theList = []



    for i in Schedule.objects.filter(user_id=curr_ID):
        anotherList = ""    
        #anotherList+=str(i.id)
        if i.day==1:
            anotherList+="M"
        elif i.day==2:
            anotherList+="T"
        elif i.day==3:
            anotherList+="W"
        elif i.day==4:
            anotherList+="H"
        elif i.day==5:
            anotherList+="F"
        elif i.day==6:
            anotherList+="S"
        anotherList+=str((i.hour))

        theList.append(anotherList)

    toPass = ""
    for x in xrange(len(theList)):
        toPass+=str(theList[x])
        if x != len(theList)-1:
            toPass+=","
    return render(request, 'std/profile.html', {'uID': curr_ID, 'sched': toPass})
    #sched parameter in return is the schedule of user


def register(request):
    #to do: add error detection for user creation
    if request.POST.get('passw')!=request.POST.get('passw2'):
        return render(request, 'std/login.html', {"passerror": 1})
    try:
        userExist =  User.objects.get(username=request.POST.get('uname'))
        return render(request, 'std/login.html', {"passerror": 2})
    except:
        User.create(request.POST.get('uname'), request.POST.get('passw'), request.POST.get('identity'))    
        return render(request, 'std/index.html')

def home(request):
    return render(request, 'std/home.html')

def editprofile(request):
	#curr_ID = request.session['curr_ID']
	try:
		curr_ID = request.session['curr_ID']
	except:
		return redirect(index)
		
	theList = []
	for i in Schedule.objects.filter(user_id=curr_ID):
		anotherList = "" 
		if i.day==1:
			anotherList+="M"
		elif i.day==2:
			anotherList+="T"
		elif i.day==3:
			anotherList+="W"
		elif i.day==4:
			anotherList+="H"
		elif i.day==5:
			anotherList+="F"
		elif i.day==6:
			anotherList+="S"
			
		anotherList+=str((i.hour))
		theList.append(anotherList)
	
	toPass=""
	for x in xrange(len(theList)):
		toPass+=str(theList[x])
		if x != len(theList)-1:
			toPass+=","
	return render(request, 'std/editprofile.html',{'uID': curr_ID, 'sched': toPass})

def saveprofile(request):
    curr_ID = request.session['curr_ID']
    currSched = request.POST.get('schedule')
    

    newSched = currSched.split(',')
    parsed = []    
    for i in xrange(len(newSched)):
        toAppend = []
        
        if newSched[i][0] == 'M':
            toAppend.append(1)
        elif newSched[i][0] == 'T':
            toAppend.append(2)
        elif newSched[i][0] == 'W':
            toAppend.append(3)
        elif newSched[i][0] == 'H':
            toAppend.append(4)
        elif newSched[i][0] == 'F':
            toAppend.append(5)
        elif newSched[i][0] == 'S':
            toAppend.append(6)

        time = int(newSched[i][1:])
        toAppend.append(time)
        parsed.append(toAppend)

    #use kyle method here
    Schedule.objects.filter(user_id=curr_ID).delete()
    for x in xrange(len(newSched)):
        Schedule.add_sched(curr_ID, parsed[x][0], parsed[x][1])

    return redirect(profile)
#def createMeetUpSchedule(request):
    #getting of data here
    #put the add sched function
    #alert other users
    #stuff

def logout(request):
    del request.session['curr_ID']
    return redirect(index)