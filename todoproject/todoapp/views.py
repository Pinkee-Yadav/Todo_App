from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegisterForm, TaskForm
from .models import Task
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.urls import reverse

def register_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful. Welcome!')
            return redirect('index')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('index')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('index')
        else:
            messages.error(request, 'Invalid username or password')
    else:
      form = AuthenticationForm()
    return render(request, 'login.html', {'form': form}) 

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')       

@login_required
def index(request):
    filter_q = request.GET.get('filter', 'all')
    if filter_q == 'completed':
        tasks = request.user.tasks.filter(completed=True).order_by('-updated_at')
    elif filter_q == 'active':
        tasks = request.user.tasks.filter(completed=False).order_by('-created_at')
    else:
        tasks = request.user.tasks.all().order_by('-created_at')

    form = TaskForm()
    return render(request, 'index.html', {'tasks': tasks, 'form': form, 'filter_q': filter_q})

@login_required
def add_task(request):
    if request.method == 'POST':
       form = TaskForm(request.POST)
       if form.is_valid():
           task = form.save(commit=False)
           task.user = request.user
           task.save()
           messages.success(request, 'Task added')
       else:
           messages.error(request, 'Error adding task')
    return redirect('index')


@login_required
def edit_task(request, pk):
    task = get_object_or_404(Task, id=pk, user=request.user)
    if request.method == "POST":
        form = TaskForm(request.POST, instance=task)  
        if form.is_valid():
            form.save() 
            messages.success(request, 'Task updated')
            return redirect('index')
    else:
        form = TaskForm(instance=task)

    return render(request, 'edit_task.html', {'form': form, 'task': task})





@login_required
def delete_task(request, pk):
    task = get_object_or_404(Task, pk=pk, user=request.user)
    if request.method == 'POST':
       task.delete()
       messages.success(request, 'Task deleted')
       return redirect('index')
    return render(request, 'confirm_delete.html', {'task': task})


@login_required
def toggle_complete(request, pk):
    # Works with POST (recommended). If you used an <a> link, allow GET too.
    task = get_object_or_404(Task, pk=pk, user=request.user)
    task.completed = not task.completed
    task.save(update_fields=['completed', 'updated_at'])
    messages.success(request, f"Marked as {'Completed' if task.completed else 'Active'}.")

    # return to the same filter tab user was on
    next_url = request.POST.get('next') or request.GET.get('next') or reverse('index')
    return redirect(next_url)
    