from django.http import HttpResponseRedirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from .forms import PostForm, CommentForm
from .filters import *
from .models import *


class PostsList(ListView):
    model = Post
    template_name = 'posts.html'
    context_object_name = 'posts'
    ordering = '-dateCreation'
    paginate_by = 7

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_posts'] = Post.objects.all()
        return context

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.kwargs['pk']})



class CommentsList(LoginRequiredMixin, ListView):
    model = Comment
    template_name = 'mycomments.html'
    context_object_name = 'mycomments'
    ordering = '-comment_dateCreation'
    paginate_by = 4

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context

    def get_queryset(self):
        comments = Comment.objects.filter(comment_post__author=self.request.user)
        self.filterset = CommentFilter(self.request.GET, queryset=comments)
        return self.filterset.qs

    def post(self, request, *args, **kwargs):
        comment_id = request.POST['comment']
        comment = Comment.objects.get(id=comment_id)
        if comment.accepted:
            comment.accepted = False
        else:
            comment.accepted = True
        comment.save()
        return super().get(request, *args, **kwargs)

    def get_success_url(self):
        return reverse('/mycomments')


class CommentCreate(CreateView):
    model = Comment
    template_name = 'post.html'
    form_class = CommentForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def get_success_url(self):
        return reverse('comment_sent_for_approval')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.comment_author = self.request.user
        self.object.comment_post = Post.objects.get(id=self.kwargs.get('pk'))
        self.object.accepted = False
        return super().form_valid(form)


class CommentForApproval(LoginRequiredMixin, ListView):
    model = Comment
    context_object_name = 'comments'
    template_name = 'commentsentforapproval.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context


class PostDetail(DetailView, CommentCreate):
    model = Post
    template_name = 'post.html'
    context_object_name = 'post'


class PostCreate(LoginRequiredMixin, CreateView):
    model = Post
    template_name = 'createpost.html'
    context_object_name = 'post_create'
    form_class = PostForm
    success_url = '/'

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = User.objects.get(id=self.request.user.id)
        self.object.save()
        return super().form_valid(form)


class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    raise_exception = True
    template_name = 'editpost.html'
    form_class = PostForm

    def post(self, request, *args, **kwargs):
        post = Post.objects.get(id=request.get_full_path().split("/")[2])
        post.title = request.POST['title']
        post.text = request.POST['text']
        post.category = request.POST['category']
        post.save()
        return HttpResponseRedirect(f"../{post.id}")


class PostDelete(LoginRequiredMixin, DeleteView):
    model = Post
    template_name = 'deletepost.html'
    context_object_name = 'post'
    queryset = Post.objects.all()

    def get_success_url(self):
        return reverse('posts')


