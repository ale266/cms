from django.db import models
import uuid
from django.utils.text import slugify
from django.urls import reverse
from ckeditor.fields import RichTextField
from django.conf import settings
from userprofile.models import UserProfile
from django.contrib.auth.models import User #Asociamos comentarios a usuarios


# Create your models here.
class Post(models.Model):
    writer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title  = models.CharField(max_length=500, verbose_name="Titulo")
    image = models.ImageField(upload_to='img', default= 'NULL', verbose_name="Logo")
    body = RichTextField(verbose_name="Contenido")
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField(unique=True)
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True , verbose_name="Categoria")
    likes = models.ManyToManyField(UserProfile, related_name='blog_post')
    dislikes = models.ManyToManyField(UserProfile, related_name='blog_post2')
    views = models.PositiveIntegerField(default=0) #número de visualizaciones

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()
    
    def save(self, *args, **kwargs):
        # Genera automáticamente el slug a partir del título si no se proporciona uno
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        # Devuelve la URL completa de la publicación
        return reverse('post_detail', args=[str(self.slug)])
    
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
    title = models.CharField(max_length=100 , verbose_name="Titulo")
    category_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()

    def __str__(self):
        return self.title
    

"""Creamos el modelo para comentarios
class Comentario(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    autor = models.ForeignKey(User, on_delete=models.CASCADE) #Asociamos el comentario a un usuario
    contenido_comentario = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    

def __str__(self):
        return f'Comentario de {self.autor.username} en {self.fecha_creacion}'"""
