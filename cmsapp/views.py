from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from .models import Category, Post
from .forms import PostForm
from django.utils.text import slugify
from django.contrib import messages

# Create your views here.
#solo ver los posts que estan activos, los inactivos solo lo puede ver el administrador
# def index(request):
#     posts = Post.objects.all()
#     categories = Category.objects.all()
#     context = {'posts': posts, 'categories': categories}
#     return render(request, 'cmsapp/index.html', context)

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
    post  = Post.objects.get(slug = slug )
    posts = Post.objects.exclude(post_id__exact=post.post_id)[:5] #para mostrar en recent posts solo 5 post
    total_likes = post.total_likes()
    total_dislikes = post.total_dislikes()
    context = {'post': post , 'posts' : posts, 'total_likes': total_likes, 'total_dislikes': total_dislikes}
    return render (request , 'cmsapp/detail.html', context )

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



