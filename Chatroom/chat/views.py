from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import JsonResponse
import re
from django.http import HttpResponse, HttpResponseRedirect
#import requests


def signup(request):
    if request.method == 'GET':
        return render(request, 'chat/SignUp.html')
    else:
        username = request.POST.get('username')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        f_pass = request.POST.get('f_pass')
        c_pass = request.POST.get('c_pass')
        try:
            user = User.objects.get(username=username)
            return render(request, 'chat/SignUp.html', {'message': 'Username already exists.'})
        except User.DoesNotExist:
            if f_pass != c_pass:
                return render(request, 'chat/SignUp.html', {'message': "Passwords don't match."})
            else:
                user = User.objects.create_user(username=username, first_name=first_name, last_name=last_name,
                                                email=email, password=f_pass)
                user.save()
                auth.login(request, user)
                return redirect('home')


def username_validation(request):
    if request.method == 'GET':
        try:
            user = User.objects.get(username=request.GET.get('name'))
            data = {'found': True}
        except User.DoesNotExist:
            data = {'found': False}
        return JsonResponse(data)


def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is None:
            return render(request, 'chat/SignIn.html', {'message': 'Invalid Credentials.'})
        else:
            auth.login(request, user)
            return redirect('home')

    else:
        return render(request, 'chat/SignIn.html')


def logout(request):
    if request.method == 'POST':
        auth.logout(request)
        return render(request, 'chat/SignIn.html', {'message': 'User Logged out Successfully.'})


def home(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return render(request, 'chat/Home.html')
        else:
            return redirect('signin')
    else:
        return HttpResponseRedirect('room')


def edit(request):
    if request.method == "GET":
        if request.user.is_authenticated == False:
            return render(request, 'chat/SignIn.html', {'message': 'Login to edit details.'})
        else:
            return render(request, 'chat/Edit.html')
    else:
        username = request.POST.get("username")
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        email = request.POST.get("email")
        username1 = request.user.username
        user = User.objects.get(username=username1)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save(update_fields=['first_name', 'last_name', 'email'])
        return redirect('home')


def room(request, room_name):
    return render(request, 'chat/chatroom.html', {'room_name': room_name})