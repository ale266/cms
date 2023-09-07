from django.db import models
from django.contrib.auth.models import User
import uuid

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
    
