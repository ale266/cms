from django.contrib import admin
from .models import Carrousel, Category, Post, Comment, RolUsuario

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Comment)
admin.site.register(RolUsuario)
admin.site.register(Carrousel)

