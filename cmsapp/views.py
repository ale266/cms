from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.utils.text import slugify

# Create your views here.
#solo ver los posts que estan activos, los inactivos solo lo puede ver el administrador
def index(request):
    posts = Post.objects.all()
    context = {'posts': posts}
    return render(request, 'cmsapp/index.html', context)


def detail(request, slug):
    post  = Post.objects.get(slug = slug )
    posts = Post.objects.exclude(post_id__exact=post.post_id)[:5]
    context = {'post': post , 'posts' : posts}
    return render (request , 'cmsapp/detail.html', context )

def createPost(request):
    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit = False)
            post.slug = slugify(post.title)
            post.save()
            return redirect('index')
    context = {'form': form}    
    return render(request, 'cmsapp/create.html', context)

def updatePost (request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance = post)
        if form.is_valid():
            form.save()
            return redirect('detail', slug=post.slug)

    context = {'form': form}
    return render(request, 'cmsapp/create.html', context) 

#modificar este view para que desactive los blogs en vez de eliminarlos
def deletePost(request, slug):
    post = Post.objects.get(slug=slug)
    form = PostForm(instance=post)
    if request.method == 'POST':
        post.delete()
        return redirect('index')
    context = {'form': form}
    return render(request, 'cmsapp/delete.html', context) 



