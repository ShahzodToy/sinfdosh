from django.urls import path
from .views import SignInView,SignUpView,LogoutView,ProfilePageView,EditUserView,AboutPageView
urlpatterns = [
    path('login/',SignInView.as_view(),name='login'),
    path('register/',SignUpView.as_view(),name='register'),
    path('logout/',LogoutView.as_view(),name='logout'),
    path('profile/<int:id>/',ProfilePageView.as_view(),name='profile'),
    path('edit-user/',EditUserView.as_view(),name='edit_user'),
    path('about-user/<int:id>/',AboutPageView.as_view(),name='about'),
]