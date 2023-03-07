from xmlrpc.client import Boolean
from django.db import models
from datetime import datetime
from django.contrib.auth.models import AbstractUser


# Create your models here.

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    username = models.CharField(unique=True, max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null=True, blank=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    invite_alert = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []



class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    deleted = models.BooleanField(default=False)
    
    def __str__(self):
        return self.name

class Team(models.Model):
    team_leaders = models.ManyToManyField(User, related_name='team_leaders', blank=True)
    team_name = models.CharField(max_length=200)
    team_name_shortcut = models.CharField(max_length=4)
    team_members = models.ManyToManyField(User, related_name='team_members', blank=True)
    invited = models.ManyToManyField(User, related_name='invited', blank=True)

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room,null=True, on_delete=models.DO_NOTHING)
    title = models.CharField(max_length=200)
    body = models.TextField(null=True, blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['deadline','-done', '-updated', '-created']

    def __str__(self):
        return self.title[0:50]

class Team_task(models.Model):
    team_members = models.ManyToManyField(User, blank=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    title = models.TextField()
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)
    done = models.DateTimeField(auto_now=True)
    deadline = models.DateTimeField()
    archived = models.BooleanField(default=False)