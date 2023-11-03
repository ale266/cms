from django.db import models
import uuid
from django.contrib.auth.models import User, Permission, Group

from permisos.models import RolesdeSistema


# Create your models here.

class UserProfile (models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Usuario")
    name = models.CharField(max_length=200, verbose_name="Nombre")
    email=models.EmailField(max_length=200, verbose_name="Email")
    username= models.CharField(max_length=200, verbose_name="Nombre de Usuario")
    profession = models.CharField(max_length=200, verbose_name="Profesion")
    picture = models.ImageField(upload_to='img', blank=True, null=True, verbose_name="Foto")
    about = models.TextField(verbose_name="Sobre mi")
    profile_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True, primary_key=True)
    # df_rol = models.ForeignKey('Rol',on_delete=models.CASCADE,default=2)
    @property
    def pictureUrl(self):
        try:
            url = self.picture.url
        except:
            url = ''
        return url

    def __str__(self):
        return self.username
    

    
    #asignar varios roles
    def asignar_roles_usuarios(self,roles):
          
     """
     Funcion para asignar varios roles a un usuario
     """
     
     for r in roles:
        rol = RolesdeSistema.objects.get(id=r)
        group = Group.objects.get(name=rol.nombre)
        self.user.groups.add(group)
       

    def desasignar_rol(self,rol_id):
        """
         Funcion que permite quitar un rol a un usuario
        """

        rol = RolesdeSistema.objects.get(id = rol_id)
        grupo = Group.objects.get(name = rol.nombre)
        self.user.groups.remove(grupo)


class Notificaciones(models.Model):
    """
    Modelo para la implementacion de notificaciones para los usuarios del sistema
    """
    leido = models.BooleanField(default=False)
    mensaje = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    post = models.TextField()
    usuario = models.ForeignKey(User,on_delete = models.CASCADE)
   

    def __str__(self):
        return self.mensaje
 
          

# class RolUsuario(models.Model):
#     """
#     Modelo para la clase de RolUsuario con los campos necesarios para el mismo
#     """
#     miembro = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
#     roles = models.ManyToManyField(RolesdeSistema)   
 
#     def __str__(self):
#         #retorna el nombre de los roles de usuario

#         return ''.join([rol for rol in self.roles.all()])
 