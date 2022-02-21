from rest_framework.views import APIView
from rest_framework.response import Response
from .models import User, Comment, Post
from .serializers import UserSerializer, CommentSerializer, PostSerializer

# Create your views here.

class PostList(APIView):
  queryset = Post.objects.all()

  def get(self, request):
    all_queryset_posts = list(self.queryset.all())
    serialized_posts = []

    for post in all_queryset_posts:
      serialized_post = PostSerializer(post).data
      serialized_posts.append({ 'id': serialized_post['id'], 'title': serialized_post['title'] })
    
    return Response(serialized_posts)

class PostDetail(APIView):
  queryset = Post.objects.all()

  def get(self, request, pk):
    post = self.queryset.get(id=pk)
    post = PostSerializer(post).data
    return Response(post)

