from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Room, Task , User, Team, Team_task
from .forms import RoomForm, UserForm, MyUserCreationForm, TaskForm, TeamForm, Team_TaskForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout

# Create your views here.

@login_required(login_url='/login/')
def home(request):
    tasks = Task.objects.filter(archived=False).filter(user=request.user)
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    teams = Team.objects.filter(team_members = request.user)
    room_tasks = tasks

    context = {'tasks':tasks, 'rooms':rooms,
               'room_tasks':room_tasks, 'teams':teams}
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
    teams = Team.objects.filter(team_members = request.user)
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    room = Room.objects.get(id=pk)
    room_tasks = room.task_set.filter(archived = False).order_by('-created')
    task_count = room_tasks.count()

    context = {'tasks':tasks, 'room': room, 'rooms':rooms, 'room_tasks': room_tasks, 'task_count':task_count, 'teams':teams}
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
    tasks = Task.objects.filter(archived=False).filter(user=request.user)
    teams = Team.objects.filter(team_members = request.user)
    user = User.objects.get(id=pk)
    context={'user':user, 'rooms':rooms, 'teams':teams,'tasks':tasks}
    return render(request, 'api/profile.html', context)

def archivesPage(request, pk):
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    teams = Team.objects.filter(team_members = request.user)
    tasks = Task.objects.filter(archived=False).filter(user=request.user)
    archived_tasks = Task.objects.filter(archived=True).filter(user=request.user)
    task_count = archived_tasks.count()
    user = User.objects.get(id=pk)

    context = {'task_count':task_count,'archived_tasks':archived_tasks,'user':user,'rooms':rooms,
               'tasks':tasks, 'teams':teams}
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


@login_required(login_url='login')
def createTeam(request):
    form = TeamForm()
    if request.method == 'POST':

        team = Team.objects.create(
            team_name = request.POST.get('team_name'),
            team_name_shortcut = request.POST.get('team_name_shortcut'),
        )
        team.team_leaders.add(request.user)
        team.team_members.add(request.user)

        return redirect('home')
    context = {'form': form}
    return render(request, 'api/team_form.html', context)

def team(request, pk):
    teams = Team.objects.filter(team_members = request.user)
    team = Team.objects.get(id=pk)
    team_tasks = Team_task.objects.filter(team=team)
    tasks = Team_task.objects.filter(team = team.pk)
    rooms = Room.objects.filter(host=request.user).filter(deleted=False)
    task_count = tasks.count()
    members = team.team_members.all()
    leaders = team.team_leaders.all()
    invited = team.invited.all()
    

    #Invite system
    if request.method == 'POST':
            invite=request.POST.get('body')
            user = User.objects.filter(username=invite)
            #Check username is valid
            if not user:
                messages.error(request, 'There is no such user')

            else:
                invite_user = User.objects.get(username = invite)
                if invite_user in members:
                    messages.error(request, 'The user is already in team.')
                elif invite_user in invited:
                    messages.error(request, "The user is already invited.")
                #If all conditions fulfiled
                else: 
                    team.invited.add(invite_user)
                    #alerts invited player about new invite
                    invite_user.invite_alert = True
                    invite_user.save()
                    messages.success(request, 'Invite sent')
    team.save()



    context = {'tasks':tasks,'rooms':rooms, 'task_count':task_count,
               'teams':teams, 'members':members,'leaders':leaders, 'team':team,
               'team_tasks':team_tasks}


    if request.user in members:

        return render(request, 'api/team.html', context)
    else:
        return HttpResponse('You are not allowed here!')
    
def createTeam_task(request):


    pk = request.GET.get("pk")
    team = Team.objects.get(id=pk)


    form = Team_TaskForm()
    
    context = {'form': form, 'team':team}

    leaders = team.team_leaders.all()

    if request.user not in leaders:
        return HttpResponse('You are not allowed here!')

    if request.method == 'POST':
        Team_task.objects.create(
            team=team,
            title=request.POST.get('title'),
            body=request.POST.get('body'),
            deadline=request.POST.get('deadline'),
            archived = False,
        )
        return redirect('team', pk)
        

    return render(request, 'api/team_task_form.html', context)


def mailBox(request):
    teams = Team.objects.filter(invited = request.user)
    #disables alert at invites button
    request.user.invite_alert = False
    request.user.save()
    context = {'teams':teams}
    return render(request, 'api/mailbox.html', context)


def inviteAccept(request, pk):
    team = Team.objects.get(id=pk)
    invited_list = team.invited.all()

    if request.user not in invited_list:
        return HttpResponse('You are not allowed here!')


    if request.method == 'GET':
        team.team_members.add(request.user)
        team.invited.remove(request.user)
        team.save()

        pk = team.id

        return redirect('team', pk)
    

    
def inviteDecline(request, pk):
    team = Team.objects.get(id=pk)
    invited_list = team.invited.all()

    if request.user not in invited_list:
        return HttpResponse('You are not allowed here!')


    if request.method == 'GET':
        team.invited.remove(request.user)
        team.save()

        return redirect('mailbox')
    
def teamList(request):
    teams = Team.objects.filter(team_members = request.user)
        
    context = {'teams': teams}

    return render(request, 'api/team_list.html', context)

def teamMembersList(request, pk):
    team = Team.objects.get(id=pk)

    members = team.team_members.all()
    if request.user not in members:
        return HttpResponse('You are not allowed here!')
    leaders = team.team_leaders.all()
    invited = team.invited.all()

    #Invite system
    if request.method == 'POST':
            invite=request.POST.get('body')
            user = User.objects.filter(username=invite)
            #Check username is valid
            if not user:
                messages.error(request, 'There is no such user')

            else:
                invite_user = User.objects.get(username = invite)
                if invite_user in members:
                    messages.error(request, 'The user is already in team.')
                elif invite_user in invited:
                    messages.error(request, "The user is already invited.")
                #If all conditions fulfiled
                else: 
                    team.invited.add(invite_user)
                    #alerts invited player about new invite
                    invite_user.invite_alert = True
                    invite_user.save()
                    messages.success(request, 'Invite sent')
    team.save()

    context = {'team': team, 'members': members, 'leaders': leaders, 'invited': invited}

    return render(request, 'api/team_members_list.html', context)