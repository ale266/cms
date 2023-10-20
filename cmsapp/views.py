from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from .models import Category, Post, Comment
from .forms import PostForm, categoryForm, PostCommentForm
from django.views import generic, View
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages
#-------------------------------------eliminar
def eliminar_tarea(request, tarea_id):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.delete()
    # Redirigir al usuario de vuelta a la página de su tablero Kanban
    messages.success(request, 'La tarea ha sido eliminada correctamente.')
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
    tareas_pendientes = Tarea.objects.filter(usuario=request.user, estado='pendiente')
    tareas_en_proceso = Tarea.objects.filter(usuario=request.user, estado='en_proceso')
    tareas_completadas = Tarea.objects.filter(usuario=request.user, estado='completada')

    return render(request, 'cmsapp/kanban_board.html', {
        'tareas_pendientes': tareas_pendientes,
        'tareas_en_proceso': tareas_en_proceso,
        'tareas_completadas': tareas_completadas,
    })

#--------------------------------------------
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

def mover_tarea(request, tarea_id, nuevo_estado):
    tarea = get_object_or_404(Tarea, id=tarea_id, usuario=request.user)
    tarea.estado = nuevo_estado
    tarea.save()
    
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
    context = {'posts': posts, 'categories': categories}
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
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            messages.info(request, 'Blog modificado exitosamente')
            return redirect('detail', slug=post.slug)

    context = {'form': form}
    return render(request, 'cmsapp/create.html', context) 

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


"""#Comentario
def detalle_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comentarios = Comentario.objects.filter(post=post)

    if request.method == 'POST':
        comentario_form = ComentarioForm(request.POST)
        if comentario_form.is_valid():
            comentario = comentario_form.save(commit=False)
            comentario.autor = request.user  # Asigna el autor actual (si se está usando autenticación de usuario)
            comentario.post = post
            comentario.save()
            return redirect('detail', pk=pk)
    else:
        comentario_form = ComentarioForm()

    return render(request, 'cmsapp/detail.html', {'post': post, 'comentarios': comentarios, 'comentario_form': comentario_form})
"""