from . import views
from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
from rest_framework_simplejwt import views as jwt_views
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterUserView.as_view(), name='register'),
    path('update/<int:pk>/', views.UpdateProfileView.as_view(), name='register'),
    path('<int:pk>/', views.postdetail, name='post_detail'),
    path('current/<str:username>/', views.CurrentUserView.as_view(), name='post_detail'),
    path('likes/<int:pk>/',views.postlike, name='likes'),
    path('api/', views.IndexPostAPI.as_view()),
    path('api/<int:pk>', views.OnePostAPI.as_view()),
    path('api/<int:pk>/update/', views.UpdatePostView.as_view()),
    path('api/add/', views.AddPostView.as_view()),
    path('api/<int:pk>/delete/', views.DeletePostView.as_view()),
    path('api/comment/', views.IndexCommentAPI.as_view()),
    path('api/<int:pk>/comment/update/', views.UpdateCommentView.as_view()),
    path('api/add/comment/', views.AddCommentView.as_view()),
    path('api/<int:pk>/comment/delete/', views.DeleteCommentView.as_view()),
    path('api/user', views.user, name='user'),
    path('token/',jwt_views.TokenObtainPairView.as_view(), name ='token_obtain_pair'),
    path('token/refresh/',jwt_views.TokenRefreshView.as_view(), name ='token_refresh')
]