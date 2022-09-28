from django.forms import ModelForm
from .models import Room, User, Task
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
