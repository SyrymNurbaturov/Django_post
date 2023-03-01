from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
        )

        user.set_password(validated_data['password'])
        user.save()

        return user

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


