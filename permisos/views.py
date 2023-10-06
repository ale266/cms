from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group

from permisos.form import NewRolForm
from userprofile.models import UserProfile
from django.contrib.auth.models import User

from .models import RolesdeSistema
from django.contrib import messages
# Create your views here.



def crear_rol (request):


    contexto = {'user': request.user}
    contexto['form'] = NewRolForm()

    if request.method == 'POST':
        form = NewRolForm(request.POST)
        if form.is_valid():
            rol = form.save()
            rol.save()
            group = Group.objects.create(name=rol.nombre)
            group.save()
            rol.darpermisos_a_grupo(group)
            messages.success(request,"El rol "+rol.nombre+ " ha sido creado satisfactoriamente")
            return redirect('listar_roles')
        else:
            contexto['mensajeError'] = 'El nombre del rol ya existe'
    else:
        contexto['form'] = NewRolForm()

    return render(request, 'permisos/crear_rol.html', contexto)


def listar_roles(request):
    """
    Vista que muestra la lista de Roles que existen dentro del Sistema.
    Argumentos:
        request: HttpRequest
    Retorna:
        HttpResponse
    """
    contexto = {
        'roles': [
            {
                'id': rol.id, 
                'nombre': rol.nombre, 
                'descripcion': rol.descripcion,
                'defecto': rol.defecto,
                'permisos': [p.name for p in rol.get_permisos()]
            }
            for rol in RolesdeSistema.objects.all().order_by('-id')
        ],
    }

    return render(request, 'permisos/listar_roles.html', contexto)



def modificar_rol(request, id_rol):
    """
    Vista que permite editar un Rol de Sistema guardado dentro del sistema. \n
    Si el metodo Http con el que se realizo la peticion fue GET se muestra la vista de edicion del rol. \n
    Si el metodo Http con el que se realizo la peticion fue POST se toman los datos recibidos y se guardan las
    modificaciones.
    Argumentos:
        request: HttpRequest peticion recibida por el servidor \n
        id_rol: int identificador unico del Rol de Sistema que se quiere modificar
    Retorna:
        HttpResponse
    """
    rol = get_object_or_404(RolesdeSistema, pk=id_rol)

    if request.method == 'POST':
        form = NewRolForm(request.POST, instance=rol)

        if form.is_valid():
            rs = form.save()
            rs.save()
            messages.success(request,"El rol se ha modificado satisfactoriamente")
            return redirect('listar_roles')
        else:
            messages.error(request,"El rol no ha sido modificado")
        contexto = {'user': request.user, 'form': form}
    else:
        contexto = {'user': request.user,
                    'form': NewRolForm(instance=rol, initial={'permisos': [r.id for r in rol.get_permisos()]})
                    }
    return render(request, 'permisos/modificar_rol.html', contexto)


def eliminar_rol(request, id_rol):
    """
    Vista que que se encarga de eliminar un Rol de Sistema si ningun usuario tiene asignado dicho rol
    Argumentos:
        request: HttpRequest \n
        id_rol: int, identificador unico del Rol de Sistema al que se esta accediendo
    Retorna:
        HttpResponse
    """
    rol = get_object_or_404(RolesdeSistema, pk=id_rol)
    contexto = {'user': request.user, 'rol': rol}

    if request.method == 'POST':
          #agregar opcion de si el rol es utilizado , no se puede eliminar
            rol.delete()
            messages.success(request,"El rol "+rol.nombre+" ha sido eliminado satisfactoriamente")
            return redirect('listar_roles')

    return render(request, 'permisos/eliminar_rol.html', contexto)




# def asignarRol(request, id_usuario):
#     """
#     Vista que donde el Scrum master puede seleccionar el rol a asignar a un usuario dentro del proyecto
#     Argumentos:request: HttpRequest
#     Return: HttpResponse
    
#     """
   
#     usuario_rol = RolUsuario.filter(miembro=id_usuario).first()
#     if request.method == 'POST':
#         form = AsignarRolForm(id_usuario, request.POST, instance=usuario_rol) 
#         if form.is_valid():
#             roles = form.cleaned_data['roles']
#             usuario_rol = form.save()
#             usuario = User.objects.get(id=id_usuario)
#             usuario_rol.miembro = usuario
#             usuario_rol.save()
#             RolUsuario.add(usuario_rol)
#             messages.success(request,"Se asigno correctamente")    
#             return redirect('listar_roles')
#     else:
#         if usuario_rol:
#             form = AsignarRolForm(id_usuario, instance=usuario_rol)
#             data = []
#             usuario = User.objects.get(id=id_usuario)
#             data = usuario_rol
#         else:
#             form = AsignarRolForm(id_usuario, )
#     contexto = {'form': form}
#     return render(request, 'permisos/asignarRol.html', contexto)
