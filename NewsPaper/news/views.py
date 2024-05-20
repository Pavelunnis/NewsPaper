from .models import Post
from .filters import PostFilter
from .forms import PostForm

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy


class NewsList(ListView):
    model = Post
    ordering = 'namePost'
    template_name = "Posts.html"
    context_object_name = 'Posts'
    paginate_by = 10

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class NewsDetail(DetailView):
    model = Post
    template_name = 'Post.html'
    context_object_name = 'Post'


class PostSearch(ListView):
    model = Post
    ordering = 'namePost'
    template_name = 'search.html'
    context_object_name = 'Posts'
    paginate_by = 10

    def get_queryset(self):
        queryset=super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostCreate(PermissionRequiredMixin, CreateView):
    raise_exception = True
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ("news.change_post")

    def form_valid(self, form):
        post = form.save(commit=False)
        if self.request.path == '/news/articles/create/':
            post.namePost = 'AC'
        post.save()

        return super().form_valid(form)


class PostUpdate(PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'post_edit.html'
    permission_required = ("news.change_post")

class PostDelete(PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('post_list')
    permission_required = ("news.change_post")
