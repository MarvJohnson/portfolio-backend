from .models import User, Comment, Post, PostSection, PostSectionContent
from rest_framework import serializers
from rest_framework_recursive.fields import RecursiveField

class RecursiveCommentSerializer(serializers.ModelSerializer):
  replies = RecursiveField('RecursiveCommentSerializer', required=False)

  class Meta:
    model = Comment
    fields = ('replies', 'text',)

class UserSerializer(serializers.ModelSerializer):
  comments = RecursiveCommentSerializer(many=True)
  
  class Meta:
    model = User
    fields = ('username', 'comments',)


class CommentSerializer(serializers.ModelSerializer):
  author = UserSerializer()
  replies = RecursiveCommentSerializer(many=True)

  class Meta:
    model = Comment
    fields = ('author', 'replies', 'text')

class TempPostSectionContentSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostSectionContent
    fields = ('type', 'content')

class TempPostSectionSerializer(serializers.ModelSerializer):
  contents = TempPostSectionContentSerializer(many=True)
  
  class Meta:
    model = PostSection
    fields = ('title', 'contents',)

class PostSerializer(serializers.ModelSerializer):
  sections = TempPostSectionSerializer(many=True)
  
  class Meta:
    model = Post
    fields = ('id', 'title', 'topic', 'sections')

class PostSectionSerializer(serializers.ModelSerializer):
  contents = TempPostSectionContentSerializer(many=True)
  
  class Meta:
    model = PostSection
    fields = ('title', 'contents')

class PostSectionContentSerializer(serializers.ModelSerializer):
  class Meta:
    model = PostSectionContent
    fields = ('type', 'content')