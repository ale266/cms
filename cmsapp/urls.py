from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('<str:categoria>', views.indexCat, name='indexCat'),
    # path('test/<str:categoria>', views.pregunta, name='test'),
    path('dislike-post/<str:slug>', views.dislikePost, name= 'dislike'),
    path('article/<str:slug>', views.detail, name= 'detail'),
    path('create-post', views.createPost, name= 'create'),
    path('update-post/<str:slug>', views.updatePost, name= 'update'),
    path('delete-post/<str:slug>', views.deletePost, name= 'delete'),
    path('like-post/<str:slug>', views.likePost, name= 'like'),
    path('dislike-post/<str:slug>', views.dislikePost, name= 'dislike'),
]