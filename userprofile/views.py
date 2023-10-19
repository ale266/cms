from django.shortcuts import get_object_or_404, render, redirect

from cmsapp.models import Post
from .models import UserProfile
from .forms import  AsignarRolForm, UpdateProfileForm, RegistrationForm
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
# Create your views here.
def profile (request, pk):
    user_profile = UserProfile.objects.get(profile_id=pk)
    context = {'profile': user_profile}
    return render(request, 'userprofile/profile.html', context)

def account(request):
    user_account = request.user.userprofile
    context = {'account': user_account}
    return render(request, 'userprofile/account.html', context)

def registration(request):
    form = RegistrationForm()
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.info(request, 'Your account has been created successfully')
            return redirect('signin')
    context = {'form': form}
    return render(request, 'userprofile/registration.html', context)

def signin(request):
    
    if request.user.is_authenticated:
        return redirect("account")
    
    if request.method=='POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('account')
        else:
            messages.warning(request, 'Invalid Credentials')
    return render(request, 'userprofile/login.html')

def signout(request):
    logout(request)
    return redirect('signin')



@login_required(login_url=login)
def UpdateProfile(request):
    profile = request.user.userprofile
    form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        form = UpdateProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.info(request, 'Perfil editado exitosamente')
            return redirect ('account')
    context = {'form': form}
    return render(request, 'userprofile/updateprofile.html', context)

@login_required(login_url=login)
def DeleteProfile(request):
    profile = request.user.userprofile
    form = UpdateProfileForm(instance=profile)
    if request.method == 'POST':
        profile.delete()
        user = request.user
        user.delete()
        messages.info(request, 'Perfil eliminado exitosamente')
        return redirect('index')
    context = {'form':form}
    return render(request, 'userprofile/deleteprofile.html', context)



def listar_usuarios(request):
  
  """
   Vista que permite al administrador del sistema listar todos los usuarios del sistema 
   Si el usuario ya tiene permiso del sistema se deshabilita el boton de dar acceso pero
   si el usuario no tiene permiso, el boton esta disponible

    :param request: HttpRequest object
    :param id: id del usuario a eliminar
    :return: HttpResponse o HttpRedirect
  """
  
  usuarios = list(User.objects.all())

  return render(request,'userprofile/listar_usuarios.html',{'usuarios':usuarios})
   



def asignar_rol_usuario(request,id):
 
  """
  Vista que permite asignar un rol a un usuario
  :param request: HttpRequest object
  :param id : id del usuario al que se le quiere aignar un rol.
  """

  user = get_object_or_404(User,pk=id) #se busca el usuario por id
  usuario = UserProfile.objects.get(username=user.username)
  if request.method == 'POST':
    form = AsignarRolForm (request.POST, usuario=usuario)
    if form.is_valid():
      usuario.asignar_roles_usuarios(form.cleaned_data.get('Roles')) #obtiene los roles seleccionado
      return redirect('lista_users')  
    
  else:
    form = AsignarRolForm(usuario=usuario)
    if form.is_valid():
        usuario.desasignar_rol(form.cleaned_data.get('Roles')) #obtiene los roles seleccionado
        return redirect('lista_users')  

  contexto = {'usuario':usuario, 'user':request.user, 'form':form}

  return render(request,'userprofile/asignar_rol.html',contexto)
