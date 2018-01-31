from django.shortcuts import render, get_object_or_404, Http404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Post, Tag

# Create your views here.

def home(request):
    posts = Post.objects.filter(draft=False)
    paginator = Paginator(posts, 3)
    tagset = Tag.objects.all()
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
        'queryset':queryset,
        'tagset':tagset,
    }
    return render(request, 'blog/home.html', context) 

def item(request, slug):
    queryset = get_object_or_404(Post, slug=slug)
    context = {
        'queryset':queryset,
    }
    if queryset.draft:
        if request.user.is_superuser:
            return render(request, 'blog/item.html', context)
        else:
            raise Http404
    else:
        return render(request, 'blog/item.html', context)

def tagsearch(request, tag):
    posts = Post.objects.filter(tag__name__contains=tag, draft=False)
    paginator = Paginator(posts, 3)
    tagset = Tag.objects.all()
    page = request.GET.get('page')
    queryset = paginator.get_page(page)
    context = {
        'queryset':queryset,
        'tagset':tagset,
    }
    return render(request, 'blog/home.html', context)
