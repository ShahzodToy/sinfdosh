from django.contrib import messages
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render,redirect
from django.views import View
from django.contrib.auth.forms import AuthenticationForm
from .forms import SignUpForm,EditUserForm
from .models import CustomUser
from friend.models import Friend_Request


class SignInView(View):
    def get(self,request):
        login_form = AuthenticationForm()
        return render(request,'users/login.html',{'form':login_form})
    def post(self,request):
        login_form = AuthenticationForm(request, data=request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data.get('username')
            password = login_form.cleaned_data.get('password')
            user = authenticate(username=username,password =password)
            if user is not None:
                login(request,user)
                messages.success(request,'You successfully logged in')
                return redirect('home')
            else:
                messages.error(request,'You are not registres yet!!!')
                return redirect('register')
        login_form = AuthenticationForm()
        return render(request,'users/login.html',{'form':login_form})



class SignUpView(View):
    def get(self,request):
        register = SignUpForm()
        return render(request,'users/register.html',{'form':register})
    def post(self,request):
        form = SignUpForm(data=request.POST)
        if form.is_valid():
            print(request.user.username)
            form.save()
            messages.success(request,'You have been registred')
            return redirect('login')
        form =SignUpForm()

        return render(request,'users/register.html',{'form':form})


class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect('home')

class ProfilePageView(LoginRequiredMixin,View):
    def get(self,request,id):
        uer_id = CustomUser.objects.get(id=id)
        return render(request,'users/profile_page.html',{'user':uer_id})


class EditUserView(View):
    def get(self,request):
        form = EditUserForm(instance=request.user)
        return render(request,'users/edit_user.html',{'form':form})

    def post(self,request):
        form = EditUserForm(instance=request.user,data=request.POST,files = request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')
        else:
            return render(request,'users/edit_user.html',{'form':form})

class AboutPageView(View):
    def get(self, request,id):
        user_id = CustomUser.objects.get(id=id)
        return render(request, 'users/about.html', {'user': user_id})





