from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import Permission, Group

# Create your models here.
class RolesdeSistema(models.Model):
    
    nombre = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Roles de Sistema')
    defecto = models.BooleanField(default=False) # indica si el rol creado es predeterminado en el sistema y no puede borrarse.
    descripcion = models.TextField(max_length=60, blank=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Indica que varios roles pueden tener varios permisos
   # rol_usuario = models.ManyToManyField(RolUsuario, blank=True)

    class Meta:
        permissions = [
            ('_acceder_al_sistema','Acceder al sistema'),
            ('_crear_usuario', 'Crear usuario'),         
        ]    

    def __str__(self):
      return self.nombre

    def asignar_permisos(self, lista_permisos):
      """
      Funcion que asigna permisos a un rol
      param: lista de permisos
      """

      for p in lista_permisos:
        perm = Permission.objects.get(codename=p) 
        self.permisos.add(perm)

    def get_permisos(self):
      """
      Método que retorna los permisos asignados al rol.
      :return: lista de permisos
      """
      return [p for p in self.permisos.all()]

    def get_nombre(self):
      return self.nombre    

    
    def darpermisos_a_grupo(self,grupo):

      """
      Funcion que asigna todos los permisos dados a un rol a un grupo relacionado a rol
      param: el rol con los permisos
      param: el grupo al que se le quiere dar los permisos
      """

      permisos = self.get_permisos()
        
      for p in permisos:
        grupo.permissions.add(p)



    def es_utilizado(self):

      """
      Funcion que verifica si un rol esta siendo utilizado
      :return: Booleano ,True si esta siendo utilizado, False caso contrario
      """
      #Busca el grupo por nombre de rol
      if not Group.objects.exists():
        grupo = Group.objects.create(name = self.nombre)
      else:                
        grupo = Group.objects.get(name= self.nombre)
    
      return grupo.user__set.all().exists() if grupo is not None else False