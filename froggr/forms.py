from django.db import models
from django.contrib.auth.models import User
from froggr.models import UserProfile, BlogPost
from django.contrib.auth.forms import UserCreationForm
from django import forms


class UserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('text', 'image')


class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ('title', 'text', 'image')
