from django.shortcuts import render, redirect
from .models import Post
from .forms import PostForm
from django.utils.text import slugify

# Create your views here.
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
