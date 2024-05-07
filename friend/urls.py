from django.urls import path
from .views import SendRequestFriend,AcceptRequestFriend,DeclineRequestFriend

urlpatterns = [

    path('friend-request/<int:id>/',SendRequestFriend.as_view(),name = 'request_user'),
    path('friend-accept/<int:id>/',AcceptRequestFriend.as_view(),name = 'accept_user'),
    path('friend-decline/<int:id>/',DeclineRequestFriend.as_view(),name = 'decline_user'),
]