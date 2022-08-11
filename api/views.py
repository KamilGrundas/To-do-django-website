from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Task , User
from .forms import RoomForm, UserForm, MyUserCreationForm, TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    rooms = Room.objects.all()
    room_count = rooms.count()
    context = {'rooms':rooms, 'room_count':room_count}
    return render(request, 'api/home.html', context)


def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        email = request.POST.get('email').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(email=email)
        except:
            messages.error(request, 'User does not exist')

        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password does not exist')

    context = {'page':page}
    return render(request, 'api/login_register.html', context)


def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'An error occured during registration :(')
    return render(request, 'api/login_register.html', {'form':form})

def userProfile(request, pk):
    user = User.objects.get(id=pk)
    context={'user':user}
    return render(request, 'api/profile.html', context)

@login_required(login_url='login')
def updateUser(request):
    user = request.user
    form = UserForm(instance=user)

    if request.method == 'POST':
        form = UserForm(request.POST, request.FILES, instance = user)
        if form.is_valid():
            form.save()
            return redirect('user-profile', pk=user.id)

    return render(request, 'api/update-user.html', {'form':form})


@login_required(login_url='login')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':

        Room.objects.create(
            host=request.user,
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )

        return redirect('home')
    context = {'form': form}
    return render(request, 'api/room_form.html', context)

def room(request, pk):
    rooms = Room.objects.all()
    room = Room.objects.get(id=pk)
    room_tasks = room.task_set.all().order_by('-created')


    context = {'room': room, 'room_tasks': room_tasks, 'rooms':rooms}
    if request.user == room.host:

        return render(request, 'api/room.html', context)
    else:
        return HttpResponse('Wypierdalaj')

def createTask(request):
    form = TaskForm()
    pk = request.GET.get("pk")
    room = Room.objects.get(id=pk)
    if request.method == 'POST':

        Task.objects.create(
            user=request.user,
            room=room,
            title=request.POST.get('title'),
            body=request.POST.get('body')
        )

        return redirect('home')
    context = {'form': form}
    return render(request, 'api/task_form.html', context)