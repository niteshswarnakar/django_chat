
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('logout/',views.logoutUser,name = 'logout'),
    path('login/',views.loginUser,name = 'login'),
    path('register/',views.registerUser,name = 'register'),
    path('', views.home,name = "home"),
    path('room/<str:pk>',views.room,name = "room"),
    path('navbar/',views.navbar,name = "navbar"),
    path('create-room/',views.createRoom,name = "create-room"),
    path('update-room/<str:pk>/',views.updateRoom ,name = "udpate-room"),
    path('delete-room/<str:pk>/',views.deleteRoom,name = "delete-room"),
    path('delete-message/<str:pk>/',views.deleteMessage,name = 'delete-message')
]
