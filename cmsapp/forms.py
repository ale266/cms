from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from permisos.models import RolesdeSistema
from .models import Post, Category, Comment, RolUsuario
from django.contrib.auth.models import User 
class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'writer', 'likes', 'dislikes', 'views', 'roles', 'usuario_roles', 'miembros']


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
    