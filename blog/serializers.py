from django.contrib.auth.models import User
from rest_framework import serializers

from .models import *


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)
    
    class Meta:
        models = User
        fields = ['id', 'username', 'password']
        
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password']
        )
        return user
    
    
class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        models = Category
        fields = ['id', 'name', 'description', 'created_at']
        read_only_fields = ['id', 'created_at']
        
        
class PostSerializer(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    
    class Meta:
        models = Post
        fields = [
            'id', 'author', 'category', 'category_name', 'title', 'content', 'status', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'author', 'created_at', 'updated_at',]
    
    
class ComentSerializers(serializers.ModelSerializer):
    author = serializers.StringRelatedField(read_only=True)
    post_title = serializers.CharField(source='post.title', read_only=True)
    
    class Meta:
        models = Comment
        fields = ['id', 'author', 'post', 'post_title', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']