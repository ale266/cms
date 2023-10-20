from django.urls import path
from . import views
urlpatterns = [
    path('', views.index, name='index'),
    path('category/<str:categoria>', views.indexCat, name='indexCat'),
    # path('test/<str:categoria>', views.pregunta, name='test'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('dislike-post/<str:slug>', views.dislikePost, name= 'dislike'),
    path('article/<str:slug>', views.detail, name= 'detail'),
    path('create-post', views.createPost, name= 'create'),
    path('update-post/<str:slug>', views.updatePost, name= 'update'),
    path('delete-post/<str:slug>', views.deletePost, name= 'delete'),
    path('publish-post/<str:slug>', views.publishPost, name='publish'),
    path('like-post/<str:slug>', views.likePost, name= 'like'),
    path('dislike-post/<str:slug>', views.dislikePost, name= 'dislike'),
    path('list-category', views.listCategory.as_view(), name= 'listCategory'),
    path('post/<slug:slug>', views.PostView.as_view(), name= 'post'),
    path('count_comments/<int:post_id>/', views.count_comments, name='count_comments'),
    path('create-category', views.createCategory, name= 'createCategory'),
    path('update-category/<str:slug>', views.updateCategory, name= 'updateCategory'),
    path('delete-category/<str:slug>', views.deleteCategory, name= 'deleteCategory'),
    path('eliminar-comentario/', views.delete_comment, name= 'delete_comment'),
    path('asignar_miembro/<str:slug>', views.asignarMiembro, name='asignar_miembro'),
    path('asignar_rol/<str:slug>/miembro/<int:id_usuario>', views.asignarRol, name='asignar_rol'),
    

]