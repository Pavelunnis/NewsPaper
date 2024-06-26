from .models import Post, Subscription, Category
from .filters import PostFilter
from .forms import PostForm
from .tasks import send_mail_for_sub_once

from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.db.models import Exists, OuterRef
from django.shortcuts import render
from django.views.decorators.csrf import csrf_protect
from django.template.loader import render_to_string
from django.shortcuts import redirect


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


@login_required
@csrf_protect
def subscriptions(request):
    if request.method == 'POST':
        category_id = request.POST.get('category_id')
        category = Category.objects.get(id=category_id)
        action = request.POST.get('action')

        if action == 'subscribe':
            Subscription.objects.create(user=request.user, category=category)
        elif action == 'unsubscribe':
            Subscription.objects.filter(
                user=request.user,
                category=category,
            ).delete()

    categories_with_subscriptions = Category.objects.annotate(
        user_subscribed=Exists(
            Subscription.objects.filter(
                user=request.user,
                category=OuterRef('pk'),
            )
        )
    ).order_by('category')
    return render(
        request,
        'subscriptions.html',
        {'categories': categories_with_subscriptions},
    )

def send_mail_for_sub(instance):
    print('Представления - начало')
    print()
    print('====================ПРОВЕРКА СИГНАЛОВ===========================')
    print()
    print('задача - отправка письма подписчикам при добавлении новой статьи')

    sub_text = instance.text

    category = Category.objects.get(pk=Post.objects.get(pk=instance.pk).category.pk)
    print()
    print('category:', category)
    print()
    subscribers = category.subscribers.all()


    print('Адреса рассылки:')
    for pos in subscribers:
        print(pos.email)

    print()
    print()
    print()
    for subscriber in subscribers:

        print('**********************', subscriber.email, '**********************')
        print(subscriber)
        print('Адресат:', subscriber.email)

        html_content = render_to_string(
            'mail.html', {'user': subscriber, 'text': sub_text[:50], 'post': instance})

        sub_username = subscriber.username
        sub_useremail = subscriber.email

        print()
        print(html_content)
        print()

        send_mail_for_sub_once.delay(sub_username, sub_useremail, html_content)


    print('Представления - конец')

    return redirect('/news/')