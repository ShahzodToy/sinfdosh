from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View
from users.models import CustomUser
from friend.models import Friend_Request

class SendRequestFriend(View):
    def get(self,request,id):
        from_user = request.user
        to_user = CustomUser.objects.get(id=id)
        frequest = Friend_Request.objects.get_or_create(from_user=from_user,to_user=to_user)
        messages.success(request, 'You successfully sent request')
        return redirect('home')


class AcceptRequestFriend(View):
    def get(self,request,id):
        frequest = Friend_Request.objects.get(id=id)
        user1 = request.user
        user2 = frequest.to_user
        user1.friends.add(user2)
        user2.friends.add(user1)
        messages.success(request, 'You successfully accepted user')
        return redirect('home')

class DeclineRequestFriend(View):
    def get(self,request,id):
        frequest = Friend_Request.objects.get(id=id)
        user1 = request.user
        user2 = frequest.from_user  # Use from_user instead of to_user for the declination
        user1.friends.remove(user2)
        frequest.delete()  # Delete the Friend_Request object
        messages.success(request, 'You successfully decline user')
        return redirect('home')


