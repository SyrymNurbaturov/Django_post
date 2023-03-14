from .models import *
from django.contrib.auth.models import User
from rest_framework import serializers
from django.contrib.auth import get_user_model
UserModel = get_user_model()
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django import forms
from datetime import *
from django.shortcuts import get_object_or_404
from rest_framework.fields import CurrentUserDefault
from django.http import HttpResponse
class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'password', 'password2', 'first_name','last_name','email')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()


        return user

    def clean_first(self):
        first = self.cleaned_data.get("first_name")
        if not first:
            raise forms.ValidationError("Kindly enter your first name !")

    def clean_last(self):
        last = self.cleaned_data.get("last_name")
        if not last:
            raise forms.ValidationError("Kindly enter your last name !")
    def clean_email(self):
        email = self.cleaned_data.get("email")
        if not email:
            raise forms.ValidationError("Kindly enter your first name !")

class UpdateUserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError({"email": "This email is already in use."})
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError({"username": "This username is already in use."})
        return value

    def update(self, instance, validated_data):
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']

        instance.save()

        return instance

class PostSerializer(serializers.ModelSerializer):
    model = Post
    title = serializers.CharField()
    author = serializers.CharField()
    body = serializers.CharField()
    publish = serializers.DateTimeField(format='%m/%d/%Y %H:%M:%S')

    class Meta:
        model = Post
        fields = ('title', 'author', 'body','publish' )


    def create(self, validated_data):
        post = Post.objects.create(
            title=validated_data['title'],
            author=User.objects.filter(username=validated_data['author']).first(),
            body=validated_data['body'],
            publish=datetime.now(),)
        post.save()
        return post

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = "__all__"
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)


