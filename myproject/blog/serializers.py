from rest_framework import serializers
from .models import *
from django.contrib.auth.models import User


class PostSerializer(serializers.Serializer):
    model = Post
    title = serializers.CharField()
    author = serializers.SerializerMethodField("get_username")
    body = serializers.CharField()
    publish = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S")

    def get_username(self, obj):
        return obj.author.username
    def create(self, validated_data):
        return Post.objects.create(**validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username']


