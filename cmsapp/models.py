from django.db import models
import uuid
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.conf import settings
from permisos.models import RolesdeSistema
from userprofile.models import UserProfile
from django.contrib.auth.models import User #Asociamos comentarios a usuarios
#-------------------------------

class Tarea(models.Model):
    ESTADOS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_proceso', 'En Proceso'),
        ('completada', 'Completada'),
    )

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='pendiente')
    eliminada = models.BooleanField(default=False)

#------------------------------------------------------

# Create your models here.
class tipoPost:
   
    TEXTO = "Texto"
    IMAGENES = "Imagenes"
    COMBINADOS = "Combinados"
    OTROS = "Otros"

tipo_choices = (
        (tipoPost.TEXTO, 'Texto'),
        (tipoPost.IMAGENES, 'Imagenes'),
        (tipoPost.COMBINADOS, 'Combinados'),
        (tipoPost.OTROS, 'Otros'),
    )
class estadoPost:
   
    CREACION = "En Creacion"
    ENEDICION = "En Edicion"
    PUBLICACION = "En publicacion"
    DESACTIVADO = "Desactivado"

estado_choices = (
        (estadoPost.CREACION, 'En Creacion'),
        (estadoPost.ENEDICION, 'En Edicion'),
        (estadoPost.PUBLICACION, 'En Publicacion'),
        (estadoPost.DESACTIVADO, 'Desactivado'),
    )
class RolUsuario(models.Model):
    """
    Modelo para la clase de RolUsuario con los campos necesarios para el mismo
    """
    miembro = models.ForeignKey(User, on_delete=models.CASCADE)
    roles = models.ManyToManyField(RolesdeSistema)   
 
    def __str__(self):
        #retorna el nombre de los roles de usuario

        return ''.join([rol for rol in self.roles.all()])
class Carrousel (models.Model):
     image = models.ImageField(upload_to='img', default= 'NULL', verbose_name="Imagen")
     description  = models.CharField(max_length=200, verbose_name="Descripcion")

     def __str__(self):
        return self.description
    
class Post(models.Model):
    writer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Creador')
    title  = models.CharField(max_length=500, verbose_name="Titulo", unique=True)
    image = models.ImageField(upload_to='img', default= 'NULL', verbose_name="Logo")
    tipo = models.CharField(max_length=20, choices=tipo_choices, 
                    default=tipoPost.TEXTO)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True , verbose_name="Categoria")
    body = models.TextField(verbose_name="Contenido", blank=True, null=True )
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    
    likes = models.ManyToManyField(UserProfile, related_name='blog_post')
    dislikes = models.ManyToManyField(UserProfile, related_name='blog_post2')
    views = models.PositiveIntegerField(default=0) #número de visualizaciones
    miembros = models.ManyToManyField(User, related_name='set_miembros', verbose_name='Miembros')
    roles = models.ManyToManyField(RolesdeSistema)
    usuario_roles = models.ManyToManyField(RolUsuario)
    estado = models.CharField(max_length=20, choices=estado_choices, 
                    default=estadoPost.CREACION)
    report_count = models.PositiveIntegerField(default=0)
    carrousel = models.ManyToManyField(Carrousel, verbose_name='Imagenes', blank=True )
    copy_count = models.PositiveIntegerField(default=0) #contador copias link

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    
    def total_copy_count(self):
        return self.copy_count
    
    def save(self, *args, **kwargs):
        # Genera automáticamente el slug a partir del título si no se proporciona uno
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Devuelve la URL completa de la publicación
        return reverse('post_detail', args=[str(self.slug)])
    
    
    def get_Writer(self):
        """
        Metodo que retorna el Usuario del Writer del post
        """
        return self.writer

    def miembros_post(self):
        
        miembros = [self.set_miembros.get(usuario=self.writer)]
        miembros.extend(list(self.set_miembros.all().filter(rol__isnull=False)))

        return miembros
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    content = models.CharField(max_length=2000, help_text='Escriba un comentario...', verbose_name="Comentario")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    post_date = models.DateTimeField(auto_now_add=True) #Fecha de creación
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-post_date'] #se ordena por fecha de creación

    def __str__(self):
        len_title = 20
        if len(self.content) > len_title:
            return self.content[:len_title] + '...'
        return self.content


class Category(models.Model):
    title = models.CharField(max_length=100 , verbose_name="Titulo", unique=True)
    category_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    

#Reportes----------------------------------------------------------------------------------
class Report(models.Model):
    REASONS = (
        ('Spam', 'Spam'),
        ('Violencia', 'Violencia'),
        ('Información falsa', 'Información falsa'),
        ('Bullying o Acoso', 'Bullying o Acoso'),
        ('Derechos de Autor', 'Derechos de Autor'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    reason = models.CharField(max_length=255, choices=REASONS)
    comment = models.TextField(max_length=200, help_text='Escriba detalladamente', default="Más detalles...")
    def __str__(self):
        return f"{self.post} - {self.reason} - {self.user.username}"