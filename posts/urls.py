from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name = 'home'),
    path('friend-list/',views.FriendFeedView.as_view(),name = 'friend_feed'),
    path('edit/<int:id>/',views.EditPostView.as_view(),name = 'edit_post'),
    path('delete/<int:id>/',views.DeletePostView.as_view(),name = 'delete'),
    path('create/',views.CreateNewPost.as_view(),name = 'create'),
    path('detail-view/<str:slug>/',views.detail_view,name = 'detail_view'),
    path('like-view/<int:id>/',views.LikeView,name = 'likes'),
    path('check-post/',views.ListUnPublishedPost,name = 'check_post'),
    path('check-post/<int:id>/',views.Published_check_post.as_view(),name = 'check_post_byadmin'),
    path('most-weekly-view/',views.trending_weekly,name = 'most_viewed_weekly'),
    path('most-monthly-view/',views.trending_monthly,name = 'most_viewed_mothly'),

]