from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from .models import Thread, Profile
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
                profile = Profile(user=user, profile_pic='avatar2.png')
                profile.save()
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
            username = request.user.username
            user = User.objects.get(username=username)
            return render(request, 'chat/Home.html', {'user': user})
        else:
            return redirect('signin')
    else:
        chat_type = request.POST.get("type")
        if chat_type == "Go to Chatroom":
            return HttpResponseRedirect('room')
        else:
            return redirect('personal')


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
        profile_pic = request.POST.get("image")
        username1 = request.user.username
        user = User.objects.get(username=username1)
        user.username = username
        user.first_name = first_name
        user.last_name = last_name
        user.email = email
        user.save(update_fields=['first_name', 'last_name', 'email'])
        profile = Profile.objects.get(user=user)
        uploaded_file = request.FILES['image']
        profile.profile_pic = uploaded_file
        profile.save(update_fields=['profile_pic'])
        return redirect('home')


def personal(request):
    if request.method == "GET":
        return render(request, 'chat/personal.html')
    else:
        username = request.POST.get('username')
        try:
            user = User.objects.get(username=username)
            return HttpResponseRedirect(username)
        except User.DoesNotExist:
            return render(request, 'chat/personal.html', {'message' : "The Username does not exist."})


def room(request, room_name):
    print(room_name)
    return render(request, 'chat/chatroom.html', {'room_name': room_name})


def personalchat(request, username):
    try:
        thread = Thread.objects.get(user1=request.user.username, user2=username)
        return render(request, 'chat/personalchat.html', {'thread': thread.chat, 'username': username})
    except Thread.DoesNotExist:
        try:
            thread = Thread.objects.get(user1=username, user2=request.user.username)
            return render(request, 'chat/personalchat.html', {'thread': thread.chat, 'username': username})
        except Thread.DoesNotExist:
            return render(request, 'chat/personalchat.html', {'username': username})