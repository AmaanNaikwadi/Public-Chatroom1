from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.models import User, auth
from .models import Thread, Profile, Photo, Group, GroupMember, Notification, GroupMessage, ThreadMessage
import re, json
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
            groups = GroupMember.objects.filter(user=user)
            p = ''
            count = 1

            for i in range(0, len(groups)):
                group = Group.objects.get(group_name=groups[i])
                last_active_time = (GroupMember.objects.get(group=group, user=user)).last_active_time
                last_message_time = group.last_message_time
                if (last_active_time < last_message_time):
                    p += str(count)+". There are unread messages in "+str(group.group_name)+" group.\n"
                    count += 1
            try:
                notification = Notification.objects.filter(user=user, read=1)
                for i in range (0, len(notification)):
                    p += str(count)+". There are unread messages from "+str(notification[0])+" .\n"
                    count += 1
            except Notification.DoesNotExist:
                pass

            return render(request, 'chat/Home.html', {'user': user, 'notifications': p})
        else:
            return redirect('signin')
    else:
        chat_type = request.POST.get("type")
        if chat_type == "Go to Chatroom":
            return HttpResponseRedirect('room')
        elif chat_type == "Join or Create Group":
            return redirect('group')
        elif chat_type == "Go to Group":
            return redirect('groupjoin')
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
    return render(request, 'chat/chatroom.html', {'room_name': room_name})



def personalchat(request, username):
    try:
        thread = Thread.objects.get(user1=request.user.username, user2=username)
        thread_message = ThreadMessage.objects.filter(thread=thread).order_by('time')
        for i in thread_message:
            if i.sender == request.user.username:
                i.ui_align = 1
            else:
                i.ui_align = 0
        return render(request, 'chat/personalchat.html', {'thread_message': thread_message, 'username': username})
    except Thread.DoesNotExist:
        try:
            thread = Thread.objects.get(user1=username, user2=request.user.username)
            thread_message = ThreadMessage.objects.filter(thread=thread).order_by('time')
            for i in thread_message:
                if i.sender == request.user.username:
                    i.ui_align = 1
                else:
                    i.ui_align = 0
            return render(request, 'chat/personalchat.html', {'thread_message': thread_message, 'username': username})
        except Thread.DoesNotExist:
            return render(request, 'chat/personalchat.html', {'username': username})


def delete_message_personal(request, username):
    if request.method == "GET":
        try:
            thread = Thread.objects.get(user1=request.user.username, user2=username)
        except Thread.DoesNotExist:
            thread = Thread.objects.get(user1=username, user2=request.user.username)
        try:
            message = request.GET.get("message")
            receipt = ThreadMessage.objects.get(thread=thread, message=message, sender=User.objects.get(username=request.user.username))
            receipt.message = "This message was deleted"
            receipt.save()
            data = {'verdict': 'Message deleted successfully.'}
        except ThreadMessage.DoesNotExist:
            data = {'verdict_fail': 'You are not the sender of the message.'}
        return JsonResponse(data)


def group(request):
    if request.method == "GET":
        return render(request, "chat/group.html")
    else:
        option_type = request.POST.get("type")
        username = request.user.username
        user = User.objects.get(username=username)
        if option_type == "Join Group":
            group_name = request.POST.get("Group_name_1")
            try:
                group = Group.objects.get(group_name=group_name)
                try:
                    group_member = GroupMember.objects.get(group=group, user=user)
                    print(group_member)
                    return render(request, 'chat/group.html', {'message': "You are already a part of group."})
                except GroupMember.DoesNotExist:
                    group_member = GroupMember(group=group, user=user)
                    group_member.save()
                    return render(request, 'chat/group.html', {'message': 'You have been added to the group successfully.'})
            except Group.DoesNotExist:
                return render(request, 'chat/group.html', {'message': 'No such group found.'})
        else:
            group_name = request.POST.get("Group_name_2")
            try:
                group = Group.objects.get(group_name=group_name)
                return render(request, 'chat/group.html', {'message': 'The group with the entered name already exists.'})
            except Group.DoesNotExist:
                group = Group(group_name=group_name)
                group.save()
                group_member = GroupMember(group=group, user=user)
                group_member.save()
                return render(request, 'chat/group.html', {'message': 'Group has been created.'})


def groupjoin(request):
    if request.method == 'GET':
        return render(request, 'chat/groupjoin.html')
    else:
        group_name = request.POST.get("group_name")
        user = User.objects.get(username=request.user.username)
        try:
            group = Group.objects.get(group_name=group_name)
            try:
                group_member = GroupMember.objects.get(group=group, user=user)
                return HttpResponseRedirect(group_name)
            except GroupMember.DoesNotExist:
                return render(request, 'chat/groupjoin.html', {'message': "You are not added to the group."})
        except Group.DoesNotExist:
            return render(request, 'chat/groupjoin.html', {'message': "No such group exists."})


def groupchat(request, group_name):
    try:
        group = Group.objects.get(group_name=group_name)
        gmessage = GroupMessage.objects.filter(group=group).order_by('time')
        for i in gmessage:
            if i.sender == User.objects.get(username=request.user.username):
                i.ui_align = 1
            else:
                i.ui_align = 0
        return render(request, 'chat/groupchat.html', {'gmessage': gmessage, 'group_name': group_name})
    except GroupMessage.DoesNotExist:
        return render(request, 'chat/groupchat.html', {'group_name': group_name})


def upload(request, username):
    if request.method == 'POST':
        if request.is_ajax():
            image = request.FILES.get('img')
            uploaded_image = Photo(img=image)
            uploaded_image.save()
            response_data = {
                'url': uploaded_image.img.url,
            }
    return JsonResponse(response_data)


def group_upload(request, group_name):
    if request.method == 'POST':
        if request.is_ajax():
            image = request.FILES.get('img')
            uploaded_image = Photo(img=image)
            uploaded_image.save()
            response_data = {
                'url': uploaded_image.img.url,
            }
    return JsonResponse(response_data)


def add_member(request, group_name):
    if request.method == 'GET':
        group = Group.objects.get(group_name=group_name)
        try:
            user = User.objects.get(username=request.GET.get('username'))
            group_member = GroupMember.objects.get(group=group, user=user)
            data = {'message': 'The user is already a part of the group.'}
        except User.DoesNotExist:
            data = {'message': 'There is no user with given username.'}
        except GroupMember.DoesNotExist:
            group_member = GroupMember(user=user, group=group)
            group_member.save()
            data = {'message': 'The user has been added to the group successfully.'}

        return JsonResponse(data)


def delete_message(request, group_name):
    if request.method == "GET":
        group = Group.objects.get(group_name=group_name)
        try:
            message = request.GET.get("message")
            receipt = GroupMessage.objects.get(group=group, message=message, sender=User.objects.get(username=request.user.username))
            receipt.message = "This message was deleted"
            receipt.save()
            data = {'verdict': 'Message deleted successfully.'}
        except GroupMessage.DoesNotExist:
            data = {'verdict_fail': 'You are not the sender of the message.'}
        return JsonResponse(data)


def leave_group(request):
    if request.method == "POST":
        username = request.user.username
        user = User.objects.get(username=username)
        group_name = request.POST.get("group_name")
        group = Group.objects.get(group_name=group_name)
        groupmember = GroupMember.objects.get(group=group, user=user)
        groupmember.delete()
        return render(request, 'chat/Home.html', {'message': "You left the group successfully."})



