from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login as auth_login
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.views.generic import ListView, CreateView
from .models import Message
from .forms import MessageForm
from django.contrib.auth.models import User
from django.db.models import Q


@login_required
def chat_view(request, username):
    user = get_object_or_404(User, username=username)
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = user
            message.save()
            return redirect('chat_view', username=username)
    else:
        form = MessageForm()

    messages = Message.objects.filter(
        Q(sender=request.user, receiver=user) |
        Q(sender=user, receiver=request.user)
    ).order_by('timestamp')

    return render(request, 'chat/chat.html', {
        'username': username,
        'user': user,
        'messages': messages,
        'form': form
    })

def index(request):
    return render(request, 'chat/index.html')


def home(request):
    return render(request, 'chat/home.html')

@login_required
def message_list_create_view(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.receiver = recipient
            message.save()
            return redirect('message_list_create')
    else:
        form = MessageForm()

    messages = Message.objects.all()
    return render(request, 'chat/message_list_create.html', {'messages': messages, 'form': form})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def user_list(request):
    users = User.objects.exclude(id=request.user.id)  # Exclude the current user from the list
    return render(request, 'chat/user_list.html', {'users': users})


@login_required
def send_message(request):
    if request.method == 'POST':
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.sender = request.user
            message.save()
            return redirect('index')  # Redirect to a page of your choice after sending
    else:
        form = MessageForm()
    return render(request, 'chat/send_message.html', {'form': form})
