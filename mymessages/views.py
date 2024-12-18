from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from .forms import CustomUserCreationForm, MessageForm
from .models import Message, Note
from .models import Note
from .forms import NoteForm

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, '註冊成功！請編輯您的個人資料。')
            return redirect('edit_profile')  # 引導到編輯個人資料頁面
    else:
        form = CustomUserCreationForm()
    return render(request, 'mymessages/signup.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('message_list')

def message_list(request):
    messages_list = Message.objects.order_by('-created_at')
    if request.method == 'POST':
        if not request.user.is_authenticated:
            messages.error(request, '請先登入')
            return redirect('login')
        
        form = MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            message.user = request.user
            message.save()
            messages.success(request, '留言成功！')
            return redirect('message_list')
    else:
        form = MessageForm()
    
    return render(request, 'mymessages/message_list.html', {
        'messages_list': messages_list, 
        'form': form
    })

@login_required
def edit_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    
    if request.method == 'POST':
        form = MessageForm(request.POST, instance=message)
        if form.is_valid():
            form.save()
            messages.success(request, '留言已更新')
            return redirect('message_list')
    else:
        form = MessageForm(instance=message)
    
    return render(request, 'mymessages/edit_message.html', {
        'form': form, 
        'message': message
    })

@login_required
def delete_message(request, message_id):
    message = get_object_or_404(Message, id=message_id, user=request.user)
    
    if request.method == 'POST':
        message.delete()
        messages.success(request, '留言已刪除')
        return redirect('message_list')
    
    return render(request, 'mymessages/delete_message.html', {'message': message})

from .forms import UserProfileForm

@login_required
def edit_profile(request):
    user = request.user
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('edit_profile')  # 假設有一個顯示個人資料的頁面
    else:
        form = UserProfileForm(instance=user)
    
    return render(request, 'mymessages/edit_profile.html', {'form': form})

@login_required
def note_list(request):
    notes = Note.objects.filter(user=request.user).order_by('-created_at')
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, '筆記已保存！')
            return redirect('note_list')
    else:
        form = NoteForm()
    
    return render(request, 'mymessages/note_list.html', {
        'notes': notes,
        'form': form
    })