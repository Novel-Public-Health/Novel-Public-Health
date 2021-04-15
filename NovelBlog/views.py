from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from .models import Post, Comment
from .forms import PostForm, CommentForm

# Create your views here.

class frontpage(ListView):
    model = Post
    template_name = 'home.html'

class ArticleDetailView(DetailView):
    model = Post
    template_name = 'post_details.html'

class AddPostView(CreateView):
    model = Post
    template_name = 'add_post.html'
    fields = '__all__'

class AddCommentView(CreateView):
    model = Comment
    form_class = CommentForm
    template_name = 'add_comment.html'

    def form_valid(self, form):
        form.instance.post_id = self.kwargs['pk']
        return super().form_valid(form)
    
    def get_absolute_url(self):
        success_url = reverse_lazy('home')
        return success_url

    
    

    
