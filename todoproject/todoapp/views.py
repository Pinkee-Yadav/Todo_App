from django.shortcuts import render, HttpResponse,redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TaskForm
from .models import Task


def home(request):
    return render(request,'index.html')


def register_view(request):

    if request.method=="POST":
       form = RegisterForm(request.POST)
       if form.is_valid():
          form.save()
          return redirect('login')
         
    else:
        form = RegisterForm()   

    return render(request,'register.html', {'form':form})


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username,password=password)
        if user:
            login(request,user)
            return redirect('home')
        else:   
            return render(request,'login.html') 
    return render(request,'login.html')


@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


def delete_task(request):
    return HttpResponse('Deleted')
