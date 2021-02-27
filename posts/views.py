from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, status
from rest_framework.response import Response

from django.shortcuts import get_object_or_404

from .models import Post, Comment, User
from .permissions import IsAuthorOrReadOnly
from .serializers import PostSerializer, CommentSerializer, UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PostViewSet(viewsets.ViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    def list(self, request):
        serializer = self.serializer_class(self.queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def perform_create(self, serializer, *args, **kwargs):
        serializer.save(author=self.request.user)

    def retrieve(self, request, pk=None):
        post = Post.objects.get(self.queryset, id=pk)
        serializer = self.serializer_class(post)
        return Response(serializer.data,)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            serializer.save(author=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, pk=None):
        post = Post.objects.get(id=pk)
        if request.user == post.author:
            serializer = self.serializer_class(
                post,
                data=request.data
            )
            if serializer.is_valid():
                serializer.save(author=request.user)
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response(status=status.HTTP_403_FORBIDDEN)

    def destroy(self, request, pk=None):
        post = Post.objects.get(id=pk)
        if request.user == post.author:
            post.delete()
            return Response(request.data, status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_403_FORBIDDEN)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly]
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        data = {
            'author': self.request.user,
            'post': self.kwargs.get(post, status.HTTP_404_NOT_FOUND),
            'created': self.kwargs.get('created', '')
        }
        serializer.save(**data)
    
    def get_queryset(self):
        post_id = self.kwargs.get('post_id', '')
        post = get_object_or_404(Post, pk=post_id)
        all_comments_of_post = post.comments.all()
        return all_comments_of_post
