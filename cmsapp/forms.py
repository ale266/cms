from django import forms
from django.forms import ModelForm
from .models import Post, Category, Comment

class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'writer', 'likes', 'dislikes']


class categoryForm(ModelForm):
    class Meta:
        model = Category
        # fields = ('title',)
        exclude = ['slug']

class PostCommentForm(forms.ModelForm):
    content = forms.CharField(label='Ingrese su comentario', widget=forms.Textarea(attrs={'rows': 2, 'cols': 97}))
    
    class Meta:
        model = Comment
        fields = ['content'] #campo del contenido
    