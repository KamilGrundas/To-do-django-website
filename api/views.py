from unicodedata import name
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .models import Room, Task , User, Archives
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
            user.save()
            login(request, user)
            Archives.objects.create(
                host = user
            )
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
    task_count = room_tasks.count()

    context = {'room': room, 'room_tasks': room_tasks, 'rooms':rooms, 'task_count':task_count}
    if request.user == room.host:

        return render(request, 'api/room.html', context)
    else:
        return HttpResponse('You are not allowed here!')

def createTask(request):
    form = TaskForm()
    pk = request.GET.get("pk")
    room = Room.objects.get(id=pk)
    if request.method == 'POST':

        Task.objects.create(
            user=request.user,
            room=room,
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            deadline=request.POST.get('deadline'),
            archived = 0,
        )

        return redirect('home')
    context = {'form': form}
    return render(request, 'api/task_form.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):

    task = Task.objects.get(id=pk)

    if request.user != task.user:
        return HttpResponse('You are not allowed here!')

# Tutaj do poprawy
    if request.method == 'POST':
        task.delete()
        pk = task.room.id
# tutaj
        rooms = Room.objects.all() 
        room = Room.objects.get(id=pk)
        room_tasks = room.task_set.all().order_by('-created')
        task_count = room_tasks.count()

        context = {'room': room, 'room_tasks': room_tasks, 'rooms':rooms, 'task_count':task_count}
        if request.user == room.host:

            return render(request, 'api/room.html', context)
        else:
            return HttpResponse('You are not allowed here!')
# do tego
        
    return render(request, 'api/delete.html', {'obj':task.title})

def userProfile(request, pk):
    rooms = Room.objects.all()
    user = User.objects.get(id=pk)
    context={'user':user, 'rooms':rooms}
    return render(request, 'api/profile.html', context)

# def archives(request, pk):

#     archives = Archives.objects.all()
#     archive = Archives.objects.get(id=pk)
#     archive_tasks = archives.task_set.all().order_by('-created')
#     task_count_a = archive_tasks.count()

#     context = {'archive': archive, 'archive_tasks': archive_tasks, 'archives':archives, 'task_count_a':task_count_a}
#     if request.user == archive.host:

#         return render(request, 'api/archives.html', context)
#     else:
#         return HttpResponse('You are not allowed here!')


@login_required(login_url='login')
def completeTask(request, pk):

    task = Task.objects.get(id=pk)

    if request.user != task.user:
        return HttpResponse('You are not allowed here!')

# Tutaj do poprawy
    if request.method == 'POST':
        task.archived = 1
        task.save()
        pk = task.room.id
# tutaj
        rooms = Room.objects.all() 
        room = Room.objects.get(id=pk)
        room_tasks = room.task_set.all().order_by('-created')
        task_count = room_tasks.count()

        context = {'room': room, 'room_tasks': room_tasks, 'rooms':rooms, 'task_count':task_count}
        if request.user == room.host:

            return render(request, 'api/room.html', context)
        else:
            return HttpResponse('You are not allowed here!')
# do tego
        
    return render(request, 'api/delete.html', {'obj':task.title})