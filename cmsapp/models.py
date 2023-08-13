from django.db import models
import uuid
from ckeditor.fields import RichTextField
from userprofile.models import UserProfile

# Create your models here.
class Post(models.Model):
    writer = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True)
    title  = models.CharField(max_length=500)
    image = models.ImageField(upload_to='img', default= 'NULL')
    body = RichTextField()
    post_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    slug = models.SlugField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL, blank=True, null=True)
    likes = models.ManyToManyField(UserProfile, related_name='blog_post')
    dislikes = models.ManyToManyField(UserProfile, related_name='blog_post2')

    def total_likes(self):
        return self.likes.count()

    def total_dislikes(self):
        return self.dislikes.count()

    def __str__(self):
        return self.title
    
class Category(models.Model):
    title = models.CharField(max_length=100)
    category_id = models.UUIDField(default=uuid.uuid4, primary_key=True, unique=True, editable=False)
    slug = models.SlugField()

    def __str__(self):
        return self.title