from django.contrib import admin
<<<<<<< HEAD
from .models import Post
=======
from .models import Category, Post
>>>>>>> 4fd213ece1917d14a2e2ebc4836d4d309639e922

# Register your models here.
class PostAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}
<<<<<<< HEAD
admin.site.register(Post, PostAdmin)
=======

class CategoryAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug':('title', )}

admin.site.register(Post, PostAdmin)
admin.site.register(Category, CategoryAdmin)
>>>>>>> 4fd213ece1917d14a2e2ebc4836d4d309639e922
