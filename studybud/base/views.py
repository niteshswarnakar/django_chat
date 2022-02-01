from email import message
from django.shortcuts import render,redirect
from django.http import HttpResponse 
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.http import  HttpResponse
from django.db.models import Q 
from django.urls import path
from .models import Message, Room, Topic
from .forms import RoomForm
from django.contrib import messages
# rooms = [
#     {'id' : 1, 'name' : 'Career Talk'},
#     {'id' : 2 ,'name' : 'Roadmap to webdevelopment'},
#     {'id' : 3, 'name' : 'Enterpreneurship'}
# ]



def loginUser(request):
    page = 'login'
    #to prevent re-logging in if user is already logged in
    if request.user.is_authenticated:
        return redirect('home')

    context = {'page':page}

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        print(username)
        
        #check is user exists or not
        try:
            user = User.objects.get(username = username)
        except:
            messages.error(request,'user doesnot exist')
        
        #if user exists
        user = authenticate(request,username = username, password=password)

        #if user is valid
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            print('password is incorrect')
            messages.error(request,'incorrect password')

    return render(request,'base/login_register.html',context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerUser(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        #check if form submitted is valid
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request,user)
            return redirect('home')
        else:
            messages.error(request,'An error occured during registration')

    context = {'form':form}
    return render(request,'base/login_register.html',context)

def home(request):
    print('request -',request)
    q = request.GET.get('q') if request.GET.get('q') !=None else ''
    print("value of q -",q)
    rooms = Room.objects.filter(
        Q(topic__name__icontains = q) |
        Q(name__icontains= q) |
        Q(description__icontains = q)
        )
    print('rooms fetched -',rooms)
    topics = Topic.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms,'topics':topics,'room_count':room_count,'user':request.user}
    return render(request,'base/home.html',context)

def room(request,pk):
    room = Room.objects.get(id = pk)
    room_messages = room.message_set.all().order_by('-created')
    participants = room.participants.all()
    if request.method == 'POST':
        message = Message.objects.create(
            user = request.user,
            room = room,
            body = request.POST.get('body')
        )

        room.participants.add(request.user)

        return redirect('room',pk = room.id)

    context = {'room':room,'room_messages':room_messages,'users':participants}
    return render(request,"base/room.html",context)

def navbar(request):
    return render(request,'navbar.html')

@login_required(login_url = 'login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        form = RoomForm(request.POST)
        print(request.POST)

        if form.is_valid():
            form.save()
            return redirect('home')


    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url = 'login')
def updateRoom(request,pk):
    room = Room.objects.get(id = pk)
    form = RoomForm(instance=room)

    #to check other than the host of the room can't update the room details
    if request.user!= room.host:
        return HttpResponse('you are not allowed to update room created by others')

    #to collect the updated request.POST data into the existing room data
    if request.method == 'POST':
        form = RoomForm(request.POST,instance=room)
        if form.is_valid():
            form.save()
            return redirect('home')
    context = {'form':form}
    return render(request,'base/room_form.html',context)


@login_required(login_url = 'login')
def deleteRoom(request,pk):
    room = Room.objects.get(id = pk)

    if request.user!= room.host:
        return HttpResponse("You are not the host of this room . so you don't have permission to delete this")

    if request.method == 'POST':
        room.delete()
        return redirect('home')
    return render(request,'base/delete.html',{'obj':room})

def deleteMessage(request,pk):
    message = Message.objects.get(id=pk)

    if request.user!=message.user:
        return HttpResponse("you can't delete this")
    
    if request.method == 'POST':
        message.delete()
        return redirect('home')

    return render(request,'base/delete.html',{'obj':message})


