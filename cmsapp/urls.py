from django.urls import path
from . import views
urlpatterns = [
<<<<<<< HEAD
    path('', views.index, name='index')
=======
    path('', views.index, name='index'),
    path('article/<str:slug>', views.detail, name= 'detail'),
    path('create-post', views.createPost, name= 'create'),
>>>>>>> 4fd213ece1917d14a2e2ebc4836d4d309639e922
]