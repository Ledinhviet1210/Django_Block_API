from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework.decorators import action
from rest_framework.response import Response
# Create your views here.
from .models import *
from .serializers import (
    RegisterSerializer,
    CategorySerializer,
    PostSerializer,
    CommentSerializers,
)
from .permissions import IsAuthorOrReadOnly


class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    
    
class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all().order_by('created_at')
    serializer_class = CategorySerializer
    
    def get_permissions(self):
        if self.action in ['list', 'retrieve']:
            return [AllowAny()]
        
        return [IsAuthenticated()]
    
    
class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    
    def get_queryset(self):
        queryset = Post.objects.all().order_by('created_at')

        if not self.request.user.is_authenticated:
            queryset = queryset.filter(status=
                                       'published')
        elif not self.request.user.is_staff:
            queryset = queryset.filter(status='published') | queryset.filter(author=self.request.user)
            
        search = self.request.query_params.get('search')
        status = self.request.query_params.get('status')
        category = self.request.query_params.get('category')
        
        if search:
            queryset = queryset.filter(title__icontains=search)
            
        if status:
            queryset = queryset.filter(status=status)
            
        if category:
            queryset = queryset.filter(category_id=category)
            
        return queryset.distinct()
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)
        
    @action(detail=True, methods=['patch'], url_path='publish')
    def publish(self, request, pk=None):
        post = self.get_object()
        post.status = 'published'
        post.save()
        
        serializer = self.get_serializer(post)
        return Response(serializer.data)
    
    
class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializers
    permission_classes = [IsAuthenticatedOrReadOnly,
                          IsAuthorOrReadOnly]
    
    def get_queryset(self):
        queryset = Comment.objects.all().order_by('created_at')
        
        post = self.request.query_params.get('post')
        
        if post:
            queryset = self.queryset.filter(post_id=post)
            
        return queryset
    
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)