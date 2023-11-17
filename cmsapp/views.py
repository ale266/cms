from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy

from permisos.models import RolesdeSistema
from django.db import models
from .models import Category, Post, Comment, RolUsuario, Report, estadoPost
from .forms import AsignarMiembroForm, AsignarRolForm, PostForm, PostUpdateForm, categoryForm, PostCommentForm, ReportForm
from django.views import generic, View
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User 
from django.http import HttpResponse
#-------------------------------------eliminar
def desactivar_post(request):
    # Redirigir al usuario de vuelta a la página de su tablero Kanban
    messages.success(request, 'El post ha sido desactivado correctamente.')
    return redirect('kanban-board')
#------------------------------------
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
        'comment_form': comment_form, 'posts' : posts, 'total_likes': total_likes, 'total_dislikes': total_dislikes,
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

#Comentarios----------------------------------------------------------------------------------------------------------------------
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
def count_comments(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments_count = Comment.objects.filter(post=post).count()
    return render(request, 'detail.html', {'comments_count': comments_count})
"""def count_comments(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments_count = Comment.objects.filter(post=post).count()
    return render(request, 'detail.html', {'comments_count': comments_count})"""

#Obtener URL
def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    
    if request.method == 'POST':
        # Incrementar el contador al hacer clic en el botón de copia
        post.copy_count += 1
        post.save()

    posts = Post.objects.exclude(post_id__exact=post.post_id)[:5] #para mostrar en recent posts solo 5 post
    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()

    context = {
        'post': post,
        'copy_count' : post.copy_count,
        'posts' : posts, 'total_likes' : total_likes, 'total_dislikes' : total_dislikes
    }
    return render(request, 'cmsapp/detail.html', context)


def createPost(request):
    profile = request.user.userprofile
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit = False)
            post.slug = slugify(post.title)
            post.writer = profile
            post.save()
            messages.info(request, 'Blog creado exitosamente')
            return redirect('create')
        else:
            messages.error(request, 'Blog no creado')
    context = {'form': form}    
    return render(request, 'cmsapp/create.html', context)

def updatePost (request, slug):
    post = Post.objects.get(slug=slug)
    post.estado = 'En Edicion'
    form = PostUpdateForm(instance=post)
    if request.method == 'POST':
        form = PostUpdateForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            messages.info(request, 'Blog modificado exitosamente')
            return redirect('detail', slug=post.slug)
    context = {'form': form}
    return render(request, 'cmsapp/update.html', context) 

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
    Donde el publicador puede publicar un proyecto
    Argumentos:request: HttpRequest
    Return: HttpResponse
    """
    
    post = get_object_or_404(Post, slug=slug)
    post.estado = 'En Publicacion'
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
    model = Category
    template_name =  'cmsapp/listCategory.html' #object_list


def createCategory(request):
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
    category = Category.objects.get(slug=slug)
    form = categoryForm(instance=category)
    if request.method == 'POST':
        category.delete()
        messages.info(request, 'Categoria eliminada exitosamente')
        return redirect('listCategory')
    context = {'form': form}
    return render(request, 'cmsapp/deleteCategory.html', context) 

 

def asignarMiembro(request, slug):
    """
    Vista que donde el Creador puede seleccionar los participantes del post
    Argumentos:request: HttpRequest
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
            return redirect('detail', slug=slug)
    contexto = {
        'form': form,
        'post': post,
    }
    return render(request, 'cmsapp/asignar_miembro.html', contexto)

def asignarRol(request, slug, id_usuario):
    """
    Vista que donde el Scrum master puede seleccionar el rol a asignar a un usuario dentro del proyecto
    Argumentos:request: HttpRequest
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
            usuario_rol.miembro = usuario
            usuario_rol.save()
            post.usuario_roles.add(usuario_rol)
            messages.success(request,"Se asigno correctamente")
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

#Reportes---------------------------------------------------------------------------------------------------
def report_post(request, slug):
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

#Estadísticas------------------------------------------------------------------------------------------------------
#Gráficos estadísticos por post
import matplotlib
matplotlib.use('Agg') #Función que indica a Matplotlib que use el backend 'Agg', que no requiere un bucle principal.
import matplotlib.pyplot as plt
from io import BytesIO
import base64

def estadisticas_post(request, slug):
    post = get_object_or_404(Post, slug = slug)
    comment_count = Comment.objects.filter(post=post).count()
    total_interacciones = post.likes.count() + post.dislikes.count() + post.views + post.copy_count + post.report_count + comment_count
    
    # Crear datos para el gráfico circular
    labels = ['Likes', 'Dislikes', 'Vistas', 'Copias de URL', 'Denuncias', 'Comentarios']
    sizes = [post.likes.count(), post.dislikes.count(), post.views, post.copy_count, post.report_count, comment_count]
    colors = ['green', 'red', 'blue', 'purple', 'orange', 'fuchsia']  # Asigna colores a cada categoría

    # Crear el gráfico circular en el hilo principal
    fig, ax = plt.subplots(figsize=(8,8))
    pie_result = ax.pie(sizes, autopct='', startangle=90, colors=colors)  # Eliminar etiquetas y porcentajes del gráfico
    wedges, _, _ = pie_result  # Obtener la variable 'wedges'
    ax.axis('equal')


     # Configurar leyenda con colores y porcentajes
    legend_labels = [f'{label}: {percentage:.1f}%' for label, percentage in zip(labels, [s / total_interacciones * 100 for s in sizes])]
    legend = ax.legend(wedges, legend_labels, title="Concepto", loc="center right", bbox_to_anchor=(1.85, 0.5))


    # Alinear los textos de la leyenda con los colores correspondientes
    for text, color in zip(legend.get_texts(), colors):
        text.set_color(color)
        text.set_size(20)

    # Ajustar el diseño para evitar solapamiento
    plt.subplots_adjust(left=0.1, right=0.6)

    # Ajustar el diseño para asegurar que la leyenda esté completamente visible
    plt.tight_layout()

    # Guardar la imagen en un objeto BytesIO
    buffer = BytesIO()
    plt.savefig(buffer, format='png')
    buffer.seek(0)
    plt.close()

    # Convertir la imagen a base64
    image_png = buffer.getvalue()
    graphic = base64.b64encode(image_png).decode()

    # Pasar la imagen a la plantilla
    context = {
        'post': post,
        'total_likes': post.likes.count(),
        'total_dislikes': post.dislikes.count(),
        'post.views': post.views,
        'post.copy_count': post.copy_count,
        'post.report_count': post.report_count,
        'comment_count': comment_count,
        'total_interacciones': total_interacciones,
        'graphic': graphic,
    }
   
    return render(request, 'cmsapp/estadisticas_post.html', context)

#Datos estadísticos general
