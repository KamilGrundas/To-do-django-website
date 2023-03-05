from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerPage, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/',views.updateUser, name="update-user"),
    path('update-rooms/',views.updateRooms, name="update-rooms"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/',views.createRoom, name="create-room"),
    path('create-task/',views.createTask, name="create-task"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('delete-task/<str:pk>/',views.deleteTask, name="delete-task"),
    path('delete-room/<str:pk>/',views.deleteRoom, name="delete-room"),
    path('complete-task/<str:pk>/', views.completeTask, name="complete-task"),
    path('archives/<str:pk>/', views.archivesPage, name="archives"),
    path('undone-task/<str:pk>/', views.undoneTask, name="undone-task"),
    path('create-team/',views.createTeam, name="create-team"),
    path('team/<str:pk>/', views.team, name="team"),
    path('create-team-task/',views.createTeam_task, name="create-team-task"),



]