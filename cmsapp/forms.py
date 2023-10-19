from django import forms
from django.forms import ModelForm
from .models import Post, Category, Comment
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


class AsignarMiembroForm(forms.ModelForm):
    """
    Form que permite asignar miembros al proyecto
    """
    disabled_fields = ('title', 'writer')

    class Meta:
        model = Post
        fields = ('title', 'miembros', 'writer')
        
    def __init__(self, *args, **kwargs):
        super(AsignarMiembroForm, self).__init__(*args, **kwargs)
        self.fields['miembros'].widget = forms.CheckboxSelectMultiple()
        self.fields['miembros'].queryset = User.objects.exclude(id=self.instance.writer.user.id)

        for field in self.disabled_fields:
            self.fields[field].disabled = True