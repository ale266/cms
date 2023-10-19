from django import forms
from django.forms import ModelForm

from permisos.models import RolesdeSistema
from .models import UserProfile
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User 


class UpdateProfileForm(ModelForm):
    class Meta:
        model = UserProfile
        exclude = ['user']

class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


class AsignarRolForm(forms.Form):
    """
    Formulario utilizado para asignar  un rol de Sistema a un Usuario.
    Clase Padre:
        form.ModelForm
    """

    def __init__(self, *args, usuario=None, **kwargs):
        """
        Constructor del Formulario.
        Agrega, en el campo 'Rol', los Roles que el Usuario podrá tener.
        """
        super(AsignarRolForm, self).__init__(*args, **kwargs)
        self.usuario = usuario
        #filtra los roles que no sean por defecto del sistema como el administrador, usuarios y sin permiso,
        self.fields['Roles'] = forms.MultipleChoiceField(widget=forms.CheckboxSelectMultiple, required=False,choices=[(p.id, p.nombre) for p in RolesdeSistema.objects.all().filter(nombre='Creador') if p.defecto==False] )
     
