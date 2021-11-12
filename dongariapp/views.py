from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post

class PostList(ListView):
    model = Post
    ordering = '-pk'
    #context_object_name = 'post_list'
    #template_name = 'dongariapp/post_list.html'

class PostDetail(DetailView):
    model = Post
    #context_object_name = 'post_list'
    #template_name = 'dongariapp/post_detail.html'

"""
def index(request):
    posts = Post.objects.all().order_by('-pk')

    return render(
        request,
        'dongariapp/post_list.html',
        {
            'posts': posts,
        }
    )

def single_post_page(request, pk):
    post = Post.objects.get(pk=pk)

    return render(
        request,
        'dongariapp/post_detail.html',
        {
            'post': post,
        }
    )
"""