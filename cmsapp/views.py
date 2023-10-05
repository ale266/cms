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


# Create your views here.
#solo ver los posts que estan activos, los inactivos solo lo puede ver el administrador
# def index(request):
#     posts = Post.objects.all()
#     categories = Category.objects.all()
#     context = {'posts': posts, 'categories': categories}
#     return render(request, 'cmsapp/index.html', context)

# VISTAS BASADAS EN FUNCIONES

#Función que se encarga de mostrar una lista de todas las publicaciones (posts) y categorías disponibles.
def index(request): 
    #obtenemos todos los objetos "post" y "category" de la BD
    posts = Post.objects.all()
    categories = Category.objects.all()
    context = {'posts': posts, 'categories': categories} #crea un diccionario "context" y lo pasa a la plantilla HTML
    return render(request, 'cmsapp/index.html', context) #renderiza al index.html y devuelve una respuesta HTTP


#Función que se encarga de mostrar una lista de publicaciones (posts) que pertenecen a una categoría determinada.
def indexCat(request, categoria):
    #obtenemos todos los objetos "post" y "category" de la BD
    posts = Post.objects.all()
    categories = Category.objects.all()
    categoryO = Category.objects.get(title=categoria)
    categoriesPosts = Post.objects.filter(category=categoryO)
    context = {'posts': posts, 'categories': categories, 'categoriesPosts': categoriesPosts} #crea un diccionario "context" y lo pasa a la plantilla HTML
    return render(request, 'cmsapp/indexCategory.html', context) #renderiza al indexCategory.html y devuelve una respuesta HTTP


def detail(request, slug):
    post  = Post.objects.get(slug = slug ) #buscamos un objeto "post" en la BD que tenga el slug proporcionado
    #excluimos el post actual de la lista "recent post" para asegurarnos de que no se muestre en recent posts
    posts = Post.objects.exclude(post_id__exact=post.post_id)[:5] #para mostrar en recent posts solo 5 post
    #realizamos el conteo de "likes" y "dislikes"
    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()
    context = {'post': post , 'posts' : posts, 'total_likes': total_likes, 'total_dislikes': total_dislikes}
    return render (request , 'cmsapp/detail.html', context )

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
    profile = request.user.userprofile #obtenemos el perfil de usuario actual
    form = PostForm() #creamos una instancia del formulario
    if request.method == 'POST': #verificamos que la solicitud sea del tipo post
        form = PostForm(request.POST, request.FILES)
        if form.is_valid: #verificamos que el formulario sea válido
            post = form.save(commit = False)
            post.slug = slugify(post.title)
            post.writer = profile #asignamos al escritor de la publicación el perfil de usuario actual
            post.save() #y guardamos el post en la BD
            messages.info(request, 'Blog creado exitosamente')
            return redirect('create') #redireccionamos al usuario a l pag de creación de blogs
        else: #si el formulario no es válido emitimos mensaje de error
            messages.error(request, 'Blog no creado')
    context = {'form': form}    #creamos diccionario
    return render(request, 'cmsapp/create.html', context) #renderizamos

#Función que permite manejar la actualización (edición) de una publicación ya existente
def updatePost (request, slug): 
    post = Post.objects.get(slug=slug) #buscamos un objeto "post" en la BD que tenga el mismo slug
    form = PostForm(instance=post) #creamos una instancia del formulario
    if request.method == 'POST': #verificamos que la solicitud sea del tipo post
        form = PostForm(request.POST, request.FILES, instance = post) 
        if form.is_valid(): #verificamos que el formulario sea válido
            form.save() #guardamos los cambios
            messages.info(request, 'Blog modificado exitosamente')
            return redirect('detail', slug=post.slug) #redireccionamos al usuario a la página de detalles de publicación

    context = {'form': form} #creamos diccionario
    return render(request, 'cmsapp/create.html', context) #renderizamos

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