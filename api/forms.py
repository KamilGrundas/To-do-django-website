from django.forms import ModelForm
from .models import Room, User, Task, Team, Team_task
from django.contrib.auth.forms import UserCreationForm



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields= ['username','email', 'password1', 'password2']



class RoomForm(ModelForm):
    class Meta:
        model = Room
        fields = '__all__'
        exclude = ['host','deleted']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['avatar', 'name','bio']

class TaskForm(ModelForm):
    class Meta:
        model = Task
        fields = ['title','body','deadline']
        
class TeamForm(ModelForm):
    class Meta:
        model = Team
        fields = ['team_name','team_name_shortcut']

class Team_TaskForm(ModelForm):
    class Meta:
        model = Team_task
        fields = ['title','body','deadline', 'team_members']



