# forms.py
from django import forms
from .models import User, Notification, Category, Post
from hashlib import sha1
from .utils import BaseImageForm


class RegisForm(forms.ModelForm):
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(render_value=True), label='密码')
    password_confirm = forms.CharField(max_length=50, widget=forms.TextInput(attrs={
        'type': 'password', 'autocomplete': 'new-password'}), label='确认密码')

    class Meta:
        model = User
        fields = ('username', 'password', 'password_confirm', 'nickname', 'stu_id', 'department')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

class LoginForm(forms.Form):
    username = forms.CharField(max_length=50, widget=forms.TextInput, label='用户名')
    password = forms.CharField(max_length=50, widget=forms.PasswordInput(render_value=True), label='密码')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            field.widget.attrs = {'class': 'form-control'}

    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return sha1(pwd.encode('utf-8')).hexdigest()


class NoticeForm(BaseImageForm):
    class Meta:
        model = Notification
        fields = ('launcher', 'type', 'title', 'text', 'additional_graphics')
        widgets = {
            'text': forms.Textarea(attrs={'class': 'fixed-height-textarea'})
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            if name == "additional_graphics":
                continue
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = current_classes + ' form-control'


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'qq', 'wechat', 'name', 'stu_id', 'department']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            current_classes = field.widget.attrs.get('class', '')
            field.widget.attrs['class'] = current_classes + ' form-control'


class PostForm(BaseImageForm):
    class Meta:
        model = Post
        fields = ["category", "title", "text", "additional_information", "additional_graphics"]
        widgets = {
            'text': forms.Textarea(attrs={'class': 'fixed-height-textarea'}),
        }

    def __init__(self, *args, **kwargs):
        cid = kwargs.pop('cid', None)
        super().__init__(*args, **kwargs)
        if cid is not None:
            self.fields['category'].initial = Category.objects.get(cid=cid)