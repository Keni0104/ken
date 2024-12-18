from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Message,Note

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'nickname']

#新增user
#id: leon
#password: 5k4g4au4au83
class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4, 
                'placeholder': '請輸入留言 (最多200字)', 
                'class': 'form-control'
            })
        }

    def clean_content(self):
        content = self.cleaned_data.get('content')
        if len(content) > 200:
            raise forms.ValidationError("留言不能超過200字。")
        return content
        
class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser    
        fields = ['first_name', 'last_name', 'email', 'birthday', 'address', 'profile_picture']
        widgets = {
            'birthday': forms.DateInput(attrs={'type': 'date'}),
            'profile_picture': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }

    def clean_profile_picture(self):
        profile_picture = self.cleaned_data.get('profile_picture')
        if profile_picture:
            if profile_picture.size > 2 * 1024 * 1024:  # 限制大小為2MB
                raise forms.ValidationError("圖片大小不能超過2MB。")
            if not profile_picture.name.endswith(('.png', '.jpg', '.jpeg', '.jfif')):  # 增加JFIF格式
                raise forms.ValidationError("僅支持PNG、JPG、JPEG和JFIF格式的圖片。")
        return profile_picture
    
class NoteForm(forms.ModelForm):
    class Meta:
        model = Note
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'rows': 4,
                'placeholder': '請輸入您的筆記',
                'class': 'form-control'
            })
        }