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
    tasks = Task.objects.filter(archived=False).filter(user=request.user)
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    room_tasks = tasks

    context = {'tasks':tasks, 'rooms':rooms,
               'room_tasks':room_tasks}
    return render(request, 'api/home.html', context)


def loginPage(request):
    page = 'login'
    context = {'page':page}
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

    #Checks that user exist

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, 'User does not exist')
            return render(request, 'api/login_register.html', context)

    #If user exist check is password correct

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Wrong password')

    
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
            user.name = user.username
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
            if user.bio == "":
                user.bio = "No information given."
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
            deleted=False,
        )

        return redirect('home')
    context = {'form': form}
    return render(request, 'api/room_form.html', context)

def room(request, pk):
    tasks = Task.objects.filter(archived=False).filter(user=request.user)
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    room = Room.objects.get(id=pk)
    room_tasks = room.task_set.filter(archived = False).order_by('-created')
    task_count = room_tasks.count()

    context = {'tasks':tasks, 'room': room, 'rooms':rooms, 'room_tasks': room_tasks, 'task_count':task_count}
    if request.user == room.host and room.deleted == False:

        return render(request, 'api/room.html', context)
    else:
        return HttpResponse('You are not allowed here!')

def createTask(request):


    pk = request.GET.get("pk")
    room = Room.objects.get(id=pk)


    form = TaskForm()
    
    context = {'form': form, 'room':room}

    if request.user != room.host:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        Task.objects.create(
            user=request.user,
            room=room,
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            deadline=request.POST.get('deadline'),
            archived = False,
        )
        return redirect('room', pk)
        

    return render(request, 'api/task_form.html', context)

@login_required(login_url='login')
def deleteTask(request, pk):

    try:


        task = Task.objects.get(id=pk)
        if request.user != task.user:
            return HttpResponse('You are not allowed here!')

        if request.method == 'POST':
            task.delete()

            if task.archived == False:
                pk = task.room.id


                return redirect('room', pk)

        #Archives page

            else:
                pk = request.user.id
                return redirect('archives', pk)


            
        return render(request, 'api/delete.html', {'obj':task.title})

    except:
        return HttpResponse('Something gone wrong!')

def userProfile(request, pk):
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    user = User.objects.get(id=pk)
    context={'user':user, 'rooms':rooms}
    return render(request, 'api/profile.html', context)

def archivesPage(request, pk):
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    tasks = Task.objects.filter(archived=False).filter(user=request.user)
    archived_tasks = Task.objects.filter(archived=True).filter(user=request.user)
    task_count = archived_tasks.count()
    user = User.objects.get(id=pk)

    context = {'task_count':task_count,'archived_tasks':archived_tasks,'user':user,'rooms':rooms,'tasks':tasks}
    if request.user.id == user.id:

        return render(request, 'api/archives.html', context)
    else:
        return HttpResponse('You are not allowed here!')

@login_required(login_url='login')
def completeTask(request, pk):

    task = Task.objects.get(id=pk)

    if request.user != task.user:
        return HttpResponse('You are not allowed here!')


    if request.method == 'GET':
        task.archived = True
        task.save()

        pk = task.room.id

        return redirect('room', pk)

@login_required(login_url='login')
def undoneTask(request, pk):

    task = Task.objects.get(id=pk)

    if request.user != task.user:
        return HttpResponse('You are not allowed here!')

    if request.method == 'GET':
        task.archived = False
        task.save()
        
        #Room page
        pk = task.room.id

        return redirect('room', pk)
     
@login_required(login_url='login')
def updateRooms(request):
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    context = {'rooms':rooms}
    return render(request, 'api/topics.html', context)


@login_required(login_url='login')
def deleteRoom(request, pk):

    # try:
    
        room = Room.objects.get(id=pk)
        tasks = Task.objects.filter(room=room).filter(archived=False)


        if request.user != room.host:
            return HttpResponse('You are not allowed here!')

        if request.method == 'POST':
            tasks.delete()
            room.deleted = True
            room.save()

            return redirect('update-rooms')
            
        return render(request, 'api/delete.html', {'obj':room.name})

    # except:
    #     return HttpResponse('Something gone wrong!')