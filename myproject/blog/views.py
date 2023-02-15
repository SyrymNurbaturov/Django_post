
from .models import Post
from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import *
from django.views.generic import *
from django.contrib.auth.views import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import logout, login

def postdetail(request, pk):
    post = Post.objects.get(id=pk)
    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()

    else:
        template_name = 'blog/post/post_detail.html'
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post).all()
        return render(request, template_name, {'post':post,'comments': comments})
    cf = CommentForm()

    context = {
        'comment_form': cf,
    }
    return render(request, 'blog/post/post_detail.html', context)

class PostListView(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 3

    login_url = '/blog/login/'
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        posts = Post.objects.all()

        return posts

def logout_user(request):
    logout(request)
    return redirect('/blog/login')

class RegisterView(CreateView):
    template_name = 'registration/registration.html'
    form_class = RegisterUserForm
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('/blog/')

@login_required(login_url='registration/login.html/')
class LoginView(LoginRequiredMixin, LoginView):
    template_name = 'registration/login.html/'
    redirect_field_name = '/blog/'

