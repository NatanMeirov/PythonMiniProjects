from django.urls import path
from MessageRestApi import views

urlpatterns = [
    path("", views.index, name = "Index Page - How To Use The System"),
    path("Index/", views.index, name = "Index Page - How To Use The System"),
    path("Homepage/", views.home, name = "Homepage - Add New User"),
    path("GetMessages/", views.get_messages_of_user, name = "User's Messages"),
    path("DisplayAllWantedMessages/", views.get_messages_of_user, name = "User's Messages"),
    path("WriteMessage/", views.write_message, name = "Write a Message"),
    path("ReadMessage/", views.read_message, name = "Read a Message"),
    path("DeleteMessage/", views.delete_message, name = "Delete a Message"),
    path("ReadSelectedMessage/", views.read_message, name = "Read the Selected Message"),
]