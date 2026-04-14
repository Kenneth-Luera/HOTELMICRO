from rest_framework import serializers
from .models import Post, PostImage

class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'user_id', 'role', 'title', 'content', 'created_at']
        read_only_fields = ['id', 'user_id', 'role', 'created_at']

class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ['id', 'post', 'image']
        read_only_fields = ['id']