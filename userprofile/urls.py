from django.urls import path
from . import views

urlpatterns = [
    path('profile/<str:pk>', views.profile, name = 'profile'),
    path('account',  views.account, name = 'account'),
    path('updateprofile',  views.UpdateProfile, name = 'updateprofile'),
    path('deleteprofile',  views.DeleteProfile, name = 'deleteprofile'),
    path('registration', views.registration, name = 'registration'),
    path('login', views.signin, name = 'signin'),
    path('logout', views.signout, name = 'signout'),
    path('listar_usuarios/',views.listar_usuarios, name='lista_users'),
    # path('asignarRol/<int:id_usuario>', views.asignarRol, name='asignarRol'),
    path('asignarRol/<int:id>',views.asignar_rol_usuario,name='asignar_rol'),
    path('verNotificacionUser/<str:username>',views.listar_notificaciones,name='listar_notis_user')
]