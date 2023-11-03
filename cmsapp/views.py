from datetime import datetime
from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy

from permisos.models import RolesdeSistema
from django.db import models

from userprofile.models import Notificaciones, UserProfile
from .models import Carrousel, Category, Post, Comment, RolUsuario, Report, estadoPost, historia
from .forms import AsignarMiembroForm, AsignarRolForm, PostForm, PostUpdateForm, categoryForm, PostCommentForm, ReportForm, imageForm
from django.views import generic, View
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User 
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Tarea

@login_required
def crear_tarea(request):
    if request.method == 'POST':
        titulo = request.POST['titulo']
        descripcion = request.POST['descripcion']
        usuario = request.user

        # Crea una nueva tarea en la base de datos
        Tarea.objects.create(titulo=titulo, descripcion=descripcion, usuario=usuario, estado='pendiente')

        # Redirige al usuario de vuelta a la página de su tablero Kanban
        return redirect('kanban-board')

    return render(request, 'cmsapp/crear_tarea.html')


#-------------------------------------------
from .models import Tarea

def kanban_board(request):
    posts_en_creacion = Post.objects.filter(estado='En Creacion')
    posts_en_edicion = Post.objects.filter(estado='En Edicion')
    posts_en_publicacion = Post.objects.filter(estado='En Publicacion')
    posts_desactivados= Post.objects.filter(estado='Desactivado')

    return render(request, 'cmsapp/kanban_board.html', {
        'posts_en_creacion': posts_en_creacion,
        'posts_en_edicion': posts_en_edicion,
        'posts_en_publicacion': posts_en_publicacion,
        'posts_desactivados': posts_desactivados
    })

#--------------------------------------------
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def mover_post(request,slug, nuevo_estado):
    post = get_object_or_404(Post, slug=slug)
    post.estado = nuevo_estado
    post.save()
    
    # Redirigir al usuario de vuelta a la página de su tablero Kanban
    return redirect(reverse('kanban-board'))



#----------------------------------------------
# Create your views here.
#solo ver los posts que estan activos, los inactivos solo lo puede ver el administrador
# def index(request):
#     posts = Post.objects.all()
#     categories = Category.objects.all()
#     context = {'posts': posts, 'categories': categories}
#     return render(request, 'cmsapp/index.html', context)

# VISTAS BASADAS EN FUNCIONES
def index(request):
    posts = Post.objects.all()
    categories = Category.objects.all()
    user = request.user
    groups = user.groups.all()
    roles = RolUsuario.roles 
    context = {'posts': posts, 'categories': categories, 'groups': groups, 'roles': roles}
    return render(request, 'cmsapp/index.html', context)

def indexCat(request, categoria):
    posts = Post.objects.all()
    categories = Category.objects.all()
    categoryO = Category.objects.get(title=categoria)
    categoriesPosts = Post.objects.filter(category=categoryO)
    context = {'posts': posts, 'categories': categories, 'categoriesPosts': categoriesPosts}
    return render(request, 'cmsapp/indexCategory.html', context)


def detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    session_key = request.session.session_key
     # Verifica si ya se ha registrado la visualización en esta sesión
    if not request.session.get(f'post_{post.post_id}_viewed', False):
        # Incrementa el contador de visualizaciones
        post.views += 1
        post.save()
        # Registra que esta sesión ha visto el post
        request.session[f'post_{post.post_id}_viewed'] = True
        
    posts = Post.objects.exclude(post_id__exact=post.post_id)[:5] #para mostrar en recent posts solo 5 post
    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()
    if request.method == 'POST':
        comment_form = PostCommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            messages.success(request, 'Comentario agregado exitosamente.')
            return redirect('detail', slug=slug)
        else:
            messages.error(request, 'Error al agregar el comentario. Por favor, verifica los datos.')
    else:
        comment_form = PostCommentForm()

    context = {
        'post': post,
        'comment_form': comment_form, 'posts' : posts, 'total_likes': total_likes, 'total_dislikes': total_dislikes
    }

    return render(request, 'cmsapp/detail.html', context)

def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        post_id = request.POST.get('post_id')
        comment = get_object_or_404(Comment, id=comment_id)
        
        # Verificar si el usuario tiene permiso para eliminar el comentario
        if comment.author == request.user:
            comment.delete()
            # Redirigir a la misma página después de eliminar el comentario
            return redirect(request.META.get('HTTP_REFERER', 'home'), pk=post_id)  # Redirigir a la página anterior, si no está disponible, redirige a 'home'
        else:
            # Manejar el caso si el usuario no tiene permiso para eliminar el comentario
            # Por ejemplo, puedes mostrar un mensaje de error o redirigir a otra página
            pass
    
    # Manejar la situación si alguien trata de acceder a esta vista directamente sin el método POST
    return redirect(request.META.get('HTTP_REFERER', 'home'), pk=post_id)  # Redirigir a la página anterior, si no está disponible, redirige a 'home'
#Comentarios
class PostDetailView(generic.DetailView):#Vista Detallada para el modelo Post -- comentarios
    model = Post
    queryset = Post.objects.filter(
         created__lte=timezone.now()
    )

    def get_content_data(self, **kwargs): 
        context = super().get_context_data(**kwargs) #se obtiene el contenido de la vista 
        context['form'] = PostCommentForm()
        return context

class PostCommentFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    template_name = 'cmsapp/detail.html'
    form_class = PostCommentForm
    model = Post

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().post(request, *args, **kwargs)

    def form_valid(self, form):
        f = form.save(commit=False)
        f.author = self.request.user
        f.post = self.object
        f.save()
        return super().form_valid(form)
        
    def get_success_url(self):
        return reverse('cms:post', kwargs={'slug': self.object.slug}) + '#comments-section'


class PostView(View):
    #metodo get
    def get(self, request, *args, **kwargs):
        view = PostDetailView.as_view()
        return view(request, *args, **kwargs)
    
    #metodo post
    def post(self, request, *args, **kwargs):
        view = PostCommentFormView.as_view()
        return view(request, *args, **kwargs)

#Contador de comentarios
def count_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments_count = Comment.objects.filter(post=post).count()
    return render(request, 'detail.html', {'comments_count': comments_count})

#Obtener URL
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'detail.html', {'post': post})


def notificacion(mensaje,usuario,post):
  
  """
  Funcion donde se crean los objetos para las notificaciones
   Arguementos:
      mensaje : lo que se guardara como notificacion
      usuario : el usuario que recibira la notificacion 
      proyecto : el nombre del proyecto asociado a la notificacion
  """
  N = Notificaciones.objects.create(usuario=usuario,mensaje=mensaje,post=post)


def createPost(request):
    """
    Vista donde el Creador puede crear un Contenido
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    profile = request.user.userprofile
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit = False)
            post.slug = slugify(post.title)
            post.writer = profile
            post.save()
            #historial
            h = historia.objects.create(post_slug = post.slug)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " creó " + "el post "
            h.evento = evento
            h.save()
            post.historial.add(h)
            post.save()
            messages.info(request, 'Blog creado exitosamente')
            return redirect('index')
        else:
            messages.error(request, 'Blog no creado')
    context = {'form': form}    
    return render(request, 'cmsapp/create.html', context)

def updatePost (request, slug):
    """
    Vista donde el Editor puede editar un Contenido
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    post = Post.objects.get(slug=slug)
    post.estado = 'En Edicion'
    form = PostUpdateForm(instance=post)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            #historial
            h = historia.objects.create(post_slug = post.slug)
            now = datetime.now()
            dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
            evento = dt_string+","+str(request.user) + " modificó " + "el post "
            h.evento = evento
            h.save()
            post.historial.add(h)
            post.save()
            messages.info(request, 'Blog modificado exitosamente')
            return redirect('detail', slug=post.slug)
    context = {'form': form}
    return render(request, 'cmsapp/update.html', context) 

def desactivar_post(request):
    """
    Vista donde se desactiva un contenido, o bien por el administrador o 
    por la cantidad de reportes superada
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    # Redirigir al usuario de vuelta a la página de su tablero Kanban
    messages.success(request, 'El post ha sido desactivado correctamente.')
    return redirect('kanban-board')



#modificar este view para que desactive los blogs en vez de eliminarlos
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        messages.info(request, 'Blog eliminado exitosamente')
        return redirect('create')
    context = {'form': form}
    return render(request, 'cmsapp/delete.html', context) 

def publishPost(request, slug):
    """
    Vista donde el publicador puede publicar un proyecto
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    """
    
    post = get_object_or_404(Post, slug=slug)
    post.estado = 'En Publicacion'
    post.save()
    #historial
    h = historia.objects.create(post_slug = post.slug)
    now = datetime.now()
    dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
    evento = dt_string+","+str(request.user) + "publicó " + "el post "
    h.evento = evento
    h.save()
    post.historial.add(h)
    post.save()
    messages.success(request, 'Post publicado satisfactoriamente')
    return redirect('detail', slug=post.slug)

def likePost(request, slug):
    post = Post.objects.get(slug=slug)
    post.likes.add(request.user.userprofile)
    return HttpResponseRedirect(reverse('detail', args=[str(slug)])) 
def dislikePost(request, slug):
    post = Post.objects.get(slug=slug)
    post.dislikes.add(request.user.userprofile)
    return HttpResponseRedirect(reverse('detail', args=[str(slug)])) 


class listCategory(ListView):
    """
    Vista donde el sistema lista los Post por categoria
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    model = Category
    template_name =  'cmsapp/listCategory.html' #object_list


def createCategory(request):
    """
    Vista donde el usuario crea una categoria de contenido
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    form = categoryForm()
    if request.method == 'POST':
        form = categoryForm(request.POST)
        if form.is_valid:
            category = form.save(commit = False)
            category.slug = slugify(category.title)
            category.save()
            messages.info(request, 'Categoria creada exitosamente')
            return redirect('listCategory')
        else:
            messages.error(request, 'Categoria no creada')
    context = {'form': form}    
    return render(request, 'cmsapp/createCategory.html', context)


def updateCategory (request, slug):
    """
    Vista donde el usuario edita una categoria de contenido
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    """
    category = Category.objects.get(slug=slug)
    form = categoryForm(instance=category)
    if request.method == 'POST':
        form = categoryForm(request.POST, instance = category)
        if form.is_valid():
            form.save()
            messages.info(request, 'Categoria modificada exitosamente')
            return redirect('listCategory')

    context = {'form': form}
    return render(request, 'cmsapp/createCategory.html', context) 

def deleteCategory(request, slug):
    """
    Vista donde el usuario elimina una categoria de contenido
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    """
    category = Category.objects.get(slug=slug)
    form = categoryForm(instance=category)
    if request.method == 'POST':
        category.delete()
        messages.info(request, 'Categoria eliminada exitosamente')
        return redirect('listCategory')
    context = {'form': form}
    return render(request, 'cmsapp/deleteCategory.html', context) 


class listImages(ListView):
    """
    Vista donde el sistema lista las imagenes del sistema 
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    model = Carrousel
    template_name =  'cmsapp/listImages.html' #object_list


def createImages(request):
    """
    Vista donde el usuario crea las imagenes del sistema 
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    form = imageForm()
    if request.method == 'POST':
        form = imageForm(request.POST, request.FILES)
        if form.is_valid:
            image = form.save(commit = False)
            image.save()
            messages.info(request, 'Imagen creada exitosamente')
            return redirect('list_images')
        else:
            messages.error(request, 'Imagen no creada')
    context = {'form': form}    
    return render(request, 'cmsapp/createImages.html', context)


def updateImages (request, id):
    """
    Vista donde el usuario edita las imagenes del sistema 
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    """
    image = Carrousel.objects.get(id=id)
    form = imageForm(instance=image)
    if request.method == 'POST':
        form = imageForm(request.POST,request.FILES, instance = image)
        if form.is_valid():
            form.save()
            messages.info(request, 'Imagen modificada exitosamente')
            return redirect('list_images')

    context = {'form': form}
    return render(request, 'cmsapp/createImages.html', context) 

def deleteImages(request, id):
    """
    Vista donde el usuario elimina las imagenes del sistema 
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    """
    image = Carrousel.objects.get(id=id)
    form = imageForm(instance=image)
    if request.method == 'POST':
        image.delete()
        messages.info(request, 'Imagen eliminada exitosamente')
        return redirect('list_images')
    context = {'form': form}
    return render(request, 'cmsapp/deleteImages.html', context) 

def asignarMiembro(request, slug):
    """
    Vista que donde el Creador puede seleccionar los miembros del post
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    """
    print(slug)
    post = get_object_or_404(Post, slug=slug)
    form = AsignarMiembroForm(instance=post)
    if request.method == 'POST':
        form = AsignarMiembroForm( instance=post, data=request.POST)
        if form.is_valid():
            miembros = form.cleaned_data['miembros']
            form.save()
            messages.success(request, 'Los miembros han sido asignados al post')
            #historial y notificaciones
            h = historia.objects.create(post_slug = post.slug)
            mensaje = str(request.user)+" te ha asignado como miembro del proyecto: "+str(post.title)
            for m in miembros :
                usuario = UserProfile.objects.get(username=m.username)
                h = historia.objects.create(post_slug = post.slug)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " asignó a " + str(m) + " al post "
                h.evento = evento
                h.save()
                post.historial.add(h)
                post.save()
                notificacion(mensaje,usuario,post.title)
            return redirect('detail', slug=slug)
    contexto = {
        'form': form,
        'post': post,
    }
    return render(request, 'cmsapp/asignar_miembro.html', contexto)

def asignarRol(request, slug, id_usuario):
    """
    Vista que donde el Creador puede seleccionar el rol a asignar a un usuario dentro del post
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    
    """
   
    post = get_object_or_404(Post, slug=slug)
    usuario_rol = post.usuario_roles.filter(miembro=id_usuario).first()
    if request.method == 'POST':
        form = AsignarRolForm(slug, id_usuario, request.POST, instance=usuario_rol) 
        if form.is_valid():
            roles = form.cleaned_data['roles']
            usuario_rol = form.save()
            usuario = User.objects.get(id=id_usuario)
            user = UserProfile.objects.get(username=usuario.username)
            usuario_rol.miembro = usuario
            usuario_rol.save()
            post.usuario_roles.add(usuario_rol)
            messages.success(request,"Se asigno correctamente")
            #historial y notificaciones
            for r in roles :
                h = historia.objects.create(post_slug = post.slug)
                now = datetime.now()
                dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
                evento = dt_string+","+str(request.user) + " asignó el rol " + str(r) + " al miembro " + str(usuario)
                mensaje = str(request.user)+" te ha asignado el rol de "+str(r)
                h.evento = evento
                h.save()
                post.historial.add(h)
                post.save()
                notificacion(mensaje,user,post.title)

            return redirect('detail', slug=slug)
    else:
        if usuario_rol:
            form = AsignarRolForm(slug, id_usuario, instance=usuario_rol)
            data = []
            usuario = User.objects.get(id=id_usuario)
            data = usuario_rol
        else:
            form = AsignarRolForm(slug, id_usuario, )
    contexto = {'form': form}
    return render(request, 'cmsapp/asignar_rol.html', contexto)

def report_post(request, slug):
    """
    Vista que donde el usuario puede reportar un post
    Argumentos:request: HttpRequest, slug: etiqueta del post
    Return: HttpResponse
    
    """
    post = Post.objects.get(slug=slug)
    if request.method == 'POST':
        form = ReportForm(request.POST)
        if form.is_valid():
            report = form.save(commit=False)
            report.user = request.user
            report.post = post
            report.save()

        # Contador de reportes
            post.report_count += 1
            post.save()
            messages.success(request, 'Gracias por informarnos!! Analizaremos y tomaremos las medidas correspondientes para ocultar/eliminar dicho contenido')
        # Verificar si el post debe desactivarse
            if post.report_count >= 8:
                post.estado = estadoPost.DESACTIVADO
                post.save()
                messages.success(request, 'Este Post fue ocultado debido a que ha alcanzado el máximo número de reportes')
      
            return redirect('detail', slug=slug)

    else:
        form = ReportForm()

    return render(request, 'cmsapp/reporte.html', {'form': form, 'post': post})


def ver_historial(request,slug):
   """
    Vista que permite visualizar el historial del post
       Argumentos:
        request: HttpRequest
        id : id del proyecto
       Return: HttpResponse    
   """
   post = get_object_or_404(Post, slug=slug)

   eventos = []

   eventos =  post.historial.all().order_by('-id')

   contexto = {'evento':eventos,'post':post}

   return render(request,'cmsapp/historial.html',contexto)
