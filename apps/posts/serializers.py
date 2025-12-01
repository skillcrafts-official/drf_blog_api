"""Serializers for apps/posts"""

from rest_framework import serializers

from apps.posts.models import PostTag, Post, PostComment, PostImage


class PostTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTag
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = '__all__'


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        fields = '__all__'


class PostImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostImage
        fields = '__all__'
