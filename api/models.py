from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(unique=True, max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

class Archives(models.Model):
    host = models.ForeignKey(User,on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.name

class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)


    def __str__(self):
        return self.name

class Team(models.Model):
    team_leaders = models.ManyToManyField(User, related_name='team_leaders', blank=True)
    team_name = models.CharField(max_length=200)
    team_name_shortcut = models.CharField(max_length=4)
    team_members = models.ManyToManyField(User, related_name='team_members', blank=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    archived = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-done', '-updated', '-created']

    def __str__(self):
        return self.body[0:50]

class Team_task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.DateTimeField(auto_now=True)