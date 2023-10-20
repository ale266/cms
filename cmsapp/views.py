from django.http import HttpResponseRedirect
from django.contrib.sessions.models import Session
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from .models import Category, Post, Comment
from .forms import AsignarMiembroForm, AsignarRolForm, PostForm, categoryForm, PostCommentForm
from django.views import generic, View
from django.views.generic import ListView, CreateView, UpdateView
from django.views.generic import FormView
from django.views.generic.detail import SingleObjectMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils import timezone
from django.utils.text import slugify
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.models import Group, Permission

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
    post.estado = 'En Creacion'
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