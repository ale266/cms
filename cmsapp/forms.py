from django import forms
from django.forms import ModelForm
from .models import Post, Category

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'writer', 'likes', 'dislikes']


class categoryForm(ModelForm):
    class Meta:
        model = Category
        # fields = ('title',)
        exclude = ['slug']