from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()

class UserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )

        return user

    class Meta:
        model = UserModel
        fields = ( "id", "username", "password")

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


