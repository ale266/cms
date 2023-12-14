from django import forms
from django.forms import ModelForm
from django.shortcuts import get_object_or_404

from permisos.models import RolesdeSistema
from .models import Post, Category, Comment, RolUsuario, Report
from django.contrib.auth.models import User 
class PostForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'writer', 'likes', 'dislikes', 'views', 'roles', 'usuario_roles', 'miembros', 'estado', 'report_count', 'copy_count']

    # def __init__(self, *args, **kwargs):
    #     super(PostForm, self).__init__(*args, **kwargs)
    #     self.fields['tipo'].disabled = True

class PostUpdateForm(ModelForm):
    class Meta:
        model = Post
        exclude = ['slug', 'writer', 'likes', 'dislikes', 'views', 'roles', 'usuario_roles', 'miembros', 'estado']

    def __init__(self, *args, **kwargs):
        super(PostUpdateForm, self).__init__(*args, **kwargs)
        # self.fields['tipo'].disabled = True


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
    Form que permite asignar miembros al post
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


class AsignarRolForm(forms.ModelForm):
    """
    Form que permite asignar roles a un miembro del post
    """
    disabled_fields = ()
    disabled_fields = ('miembro',)

    class Meta:
        model = RolUsuario
        fields = ('miembro', 'roles',)
        
    def __init__(self, slug, id_miembro, *args, **kwargs):
        super(AsignarRolForm, self).__init__(*args, **kwargs)
        self.fields['miembro'].initial = id_miembro
        self.fields['roles'].widget = forms.CheckboxSelectMultiple()
        self.fields['roles'].queryset = RolesdeSistema.objects.all()
        #roles es no requerido
        self.fields['roles'].required = False

        for field in self.disabled_fields:
            self.fields[field].disabled = True

#Reportes--------------------------------------------------------------
class ReportForm(forms.ModelForm):
    comment = forms.CharField(widget=forms.Textarea(attrs={'rows': 2, 'cols': 25}))
    class Meta:
        model = Report
        fields = ['reason', 'comment']