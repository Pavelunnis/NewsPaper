from django.views.generic import ListView, DetailView
from .models import Post


class NewsList(ListView):
    model = Post
    ordering = 'namePost'
    template_name = "Posts.html"
    context_object_name = 'Posts'


class NewsDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'Post'