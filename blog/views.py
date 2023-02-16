from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import *
from django.views.generic import *
from django.contrib.auth.views import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import logout, login
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
User = get_user_model()
from django.http import HttpResponse,HttpResponseRedirect

def postdetail(request, pk):
    post = Post.objects.get(id=pk)
    is_liked = False

    if request.method == 'POST':
        cf = CommentForm(request.POST or None)
        if cf.is_valid():
            content = request.POST.get('content')
            comment = Comment.objects.create(post=post, user=request.user, content=content)
            comment.save()

    else:
        comment_dict = {}
        com_likes = {}
        likes_count = 0
        try:
            comments = Comment.objects.filter(post=post).all()
        except Comment.DoesNotExist:
            comments = None
        else:
            for comment in comments:
                if comment.likes.filter(id=request.user.id).exists():
                    is_liked = True
                    comment_dict[comment.id] = is_liked
                    likes_count = comment.likes.count()
                    com_likes[comment.id] = likes_count
                else:
                    is_liked = False
                    comment_dict[comment.id] = is_liked
                    likes_count = comment.likes.count()
                    com_likes[comment.id] = likes_count
        template_name = 'blog/post/post_detail.html'
        post = Post.objects.get(id=pk)
        comments = Comment.objects.filter(post=post).all()

        return render(request, template_name, {'post':post,'comments': comments,'is_liked':comment_dict.items(), 'likes_count':com_likes.items(),'user':request.user.id})
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
#Dislike
# def postdislike(request, pk):

#Like
def postlike(request, pk):
    if request.method == 'POST':
        comment=get_object_or_404(Comment,id=pk)
        is_liked=False
        if comment.likes.filter(id=request.user.id).exists():
            comment.likes.remove(request.user)
            is_liked=False
        else:
            comment.likes.add(request.user)
            # notify.send(request.user, recipient=post.author, actor=request.user,
            #     verb='liked your post', nf_type='liked_post')
            is_liked=True

        return redirect('/blog/')

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

