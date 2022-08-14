from django.urls import path
from . import views


urlpatterns = [
    path('',views.home, name="home"),
    path('login/',views.loginPage, name="login"),
    path('logout/',views.logoutUser, name="logout"),
    path('register/',views.registerPage, name="register"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),
    path('update-user/',views.updateUser, name="update-user"),
    path('room/<str:pk>/', views.room, name="room"),
    path('create-room/',views.createRoom, name="create-room"),
    path('create-task/',views.createTask, name="create-task"),
    path('profile/<str:pk>/', views.userProfile, name="user-profile"),


]