from django.shortcuts import redirect,render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from rest_framework.permissions import *
from django.views.generic import *
from rest_framework.generics import CreateAPIView, UpdateAPIView, RetrieveAPIView
from django.contrib.auth.views import *
from django.contrib.auth.decorators import login_required
from .forms import *
from django.contrib.auth import logout, login, get_user_model
from rest_framework.pagination import LimitOffsetPagination, PageNumberPagination
from rest_framework.views import APIView
from .serializers import *
from rest_framework.response import Response
from django.views.generic import *
from rest_framework.request import Request
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken, BlacklistedToken

User = get_user_model()

class RegisterUserView(CreateAPIView):
    model = get_user_model()
    permission_classes = [AllowAny,]
    serializer_class = UserSerializer

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


class PostListView(LoginRequiredMixin, ListView):
    context_object_name = 'posts'
    template_name = 'blog/post/list.html'
    paginate_by = 10
    login_url = '/blog/login/'
    permission_classes = (IsAuthenticated,)
    def get_queryset(self):
        posts = Post.objects.all()
        return posts

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


class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        if self.request.data.get('all'):
            token: OutstandingToken
            for token in OutstandingToken.objects.filter(user=request.user):
                _, _ = BlacklistedToken.objects.get_or_create(token=token)
            return Response({"status": "OK, goodbye, all refresh tokens blacklisted"})
        refresh_token = self.request.data.get('refresh_token')
        token = RefreshToken(token=refresh_token)
        token.blacklist()
        return Response({"status": "OK, goodbye"})

class UpdateProfileView(UpdateAPIView):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticated,)
    serializer_class = UpdateUserSerializer

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


# API
# LoginRequiredMixin,


class IndexPostAPI(APIView, LimitOffsetPagination):
    # login_url = '/blog/login/'
    def get(self, request):
        p = Post.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 10
        paginator.page_query_param = 'page_size'
        paginator.max_page_size = 100
        result = paginator.paginate_queryset(p, request)
        serializer = PostSerializer(result, many=True)
        return Response(serializer.data)

class OnePostAPI(APIView):
    login_url = 'blog/login'
    def get(self, request, *args, **kwargs):
        pk = self.kwargs.get("pk", None)
        try:
            p = Post.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializer = PostSerializer(p)
            return Response(serializer.data)


class IndexCommentAPI(LoginRequiredMixin,APIView, LimitOffsetPagination):
    login_url = '/blog/login/'
    def get(self, request):
        c = Comment.objects.all()
        paginator = PageNumberPagination()
        paginator.page_size = 3
        paginator.page_query_param = 'page_size'
        paginator.max_page_size = 100
        result = paginator.paginate_queryset(c, request)
        serializer = CommentSerializer(result, many=True)
        return Response(serializer.data)

class AddPostView(CreateAPIView):
    model = Post
    permission_classes = [AllowAny, ]
    serializer_class = PostSerializer
    http_method_names = ['post', ]


class UpdatePostView(LoginRequiredMixin,APIView):
    def put(self, request,*args, **kwargs):
        permission_classes = (IsAdminUser,)
        pk = self.kwargs.get("pk", None)
        if not pk:
            return Response({"error":"Method not allowed"})
        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializers = PostSerializer(data=request.data, instance=instance)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)

class DeletePostView(LoginRequiredMixin,APIView):
    def delete(self, request, *args,**kwargs):
        permission_classes = (IsAdminUser,)
        pk = self.kwargs.get("pk", None)
        if not pk:
            return Response({"error":"Method not allowed"})
        try:
            instance = Post.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializers = PostSerializer(instance)
            instance.delete()
            return Response(serializers.data)

class AddCommentView(LoginRequiredMixin,APIView):
    login_url = '/blog/login/'
    def post(self, request):
        permission_classes = (IsAdminUser, )
        serializers = CommentSerializer(data=request.data)
        serializers.is_valid(raise_exception=True)
        serializers.save()

class UpdateCommentView(LoginRequiredMixin,APIView):
    login_url = '/polls/login/'
    def put(self, request,*args, **kwargs):
        permission_classes = (IsAdminUser,)
        pk = self.kwargs.get("pk", None)
        if not pk:
            return Response({"error":"Method not allowed"})
        try:
            instance = Comment.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializers = CommentSerializer(data=request.data, instance=instance)
            serializers.is_valid(raise_exception=True)
            serializers.save()
            return Response(serializers.data)

class DeleteCommentView(LoginRequiredMixin,APIView):
    login_url = '/polls/login/'
    def delete(self, request, *args,**kwargs):
        permission_classes = (IsAdminUser,)
        pk = self.kwargs.get("pk", None)
        if not pk:
            return Response({"error":"Method not allowed"})
        try:
            instance = Comment.objects.get(pk=pk)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializers = CommentSerializer(instance)
            instance.delete()

            return Response(serializers.data)


class CurrentUserView(APIView):
    def get(self, request, *args, **kwargs):
        username = self.kwargs.get("username", None)
        try:
            u = User.objects.get(username=username)
        except:
            return Response({"error": "Method not exist"})
        else:
            serializer = UserSerializer(u)
            return Response(serializer.data)

@api_view()
@permission_classes([IsAuthenticated])
@authentication_classes([BasicAuthentication])
def user(request: Request):
    return Response({
        'data': UserSerializer(request.user).data
    })