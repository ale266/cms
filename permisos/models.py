from django.db import models
from django.contrib.auth.models import User
import uuid
from django.contrib.auth.models import Permission, Group


# Create your models here.
class RolesdeSistema(models.Model):
    
    nombre = models.CharField(max_length=20, blank=False, unique=True, verbose_name='Rol de Sistema')
    defecto = models.BooleanField(default=False) # indica si el rol creado es predeterminado en el sistema y no puede borrarse.
    descripcion = models.TextField(max_length=60, blank=True)
    permisos = models.ManyToManyField(Permission, blank=True)  # Indica que varios roles pueden tener varios permisos
    # rol_usuario = models.ManyToManyField(UserProfile, blank=True)

    class Meta:
        permissions = [
            ('_acceder_al_sistema','Acceder al Sistema'),
            ('_administrar_rol','Administrar Rol'),
            ('_crear_rol', 'Crear Rol'),
            ('_modificar_rol', 'Modificar Rol'),
            ('_eliminar_rol','Eliminar Rol'),
            ('_editar_perfil', 'Editar Perfil'),
            ('_administrar_categoria', 'Administrar Categoria'),
            ('_crear_categoria', 'Crear Categoria'),
            ('_editar_categoria', 'Editar Categoria'),
            ('_eliminar_categoria', 'Eliminar Categoria'),
            ('_configurar_sitio_web', 'Configurar Sitio Web'),
            ('_administrar_contenido', 'Administrar Contenido'),
            ('_crear_contenido', 'Crear Contenido'),
            ('_editar_contenido', 'Editar Contenido'),
            ('_eliminar_contenido', 'Eliminar Contenido'),
            ('_publicar_contenido', 'Publicar Contenido'),
            ('_asignar_categoria_a_contenido', 'Asignar Categoria a Contenido'),
            ('_ver_estadistica_de_contenido', 'Ver estadistica del contenido'),
            ('_ver_numero_de_visualizaciones', 'Ver Numero de visualizaciones'),
            ('_ver_numero_de_likes', 'Ver numero de likes'),
            ('_ver_numero_de_dislikes', 'Ver numero de dislikes'),
            ('_comentar_contenido', 'Comentar contenido'),
            ('_administrar_tipo_de_contenido', 'Administar tipo de contenido'),
            ('_crear_tipo_de_contenido', 'Crear tipo de contenido'),
            ('_editar_tipo_de_contenido', 'editar tipo de contenido'),
            ('_eliminar_tipo_de_contenido', 'Eliminar tipo de contenido'),
            ('_filtrar_contenidos_por_categoria', 'Filtrar contenidos por categoria'),
            ('_filtrar_contenidos_por_tipo', 'Filtrar contenidos por tipo'),
            ('_notificar_eventos', 'Notificar eventos'), 
            ('_notificar_solicitud_de_edicion', 'Notificar solicitud de edicion'),
            ('_notificar_solicitud_de_publicacion', 'Notificar solicitud de publicacion'),
            ('_notificar_publicacion_del_contenido', 'Notificar solicitud de contenido'),
            ('_administrar_estado','Administrar estado'),
            ('_crear_estado','Crear Estado'),
            ('_modificar_estado','Modificar estado'),
            ('_eliminar_estado','Eliminar estado'),
            ('_visualizar_tablero_kanban','Visualizar tablero Kanban'),
            ('_modificar_tablero_kanban','Modificar tablero Kanban'),
            ('_visualizar_historial','Visualizar historial'),
            ('_visualizar_reporte','Visualizar reporte'),
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
