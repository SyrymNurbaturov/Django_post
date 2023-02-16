from . import views
from django.urls import re_path, path, include
from django.contrib.auth import views as auth_views
app_name = 'blog'

urlpatterns = [
    path('', views.PostListView.as_view(), name='post_list'),
    path("logout/", views.logout_user, name="logout"),
    path('login/', auth_views.LoginView.as_view(), name='login'),
    path('register/', views.RegisterView.as_view(), name='register'),
    path('<int:pk>/', views.postdetail, name='post_detail'),
    path('likes/<int:pk>/',views.postlike, name='likes')
]