from typing import Any
from urllib import request
from apps.accounts.models import User
from django.db.models.query import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound

from apps.posts.serializers import (
    PostTagSerializer, PostSerializer, PostCommentSerializer,
    PostImageSerializer
)
from apps.posts.models import (
    PostTag, Post, PostComment, PostImage
)
from apps.posts.filters import django_filters, PostFilters


class BaseModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    ...


class PostTagsView(BaseModelViewSet):
    serializer_class = PostTagSerializer

    def get_queryset(self) -> QuerySet:
        return PostTag.objects.filter(post_id=self.kwargs.get('post_id'))


class PostTagView(BaseModelViewSet):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer
    lookup_field = 'pk'


class PostsView(BaseModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filterset_class = PostFilters


class PostView(BaseModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'


class PostCommentsView(BaseModelViewSet):
    serializer_class = PostCommentSerializer

    def get_queryset(self) -> QuerySet:
        return PostComment.objects.filter(post_id=self.kwargs.get('post_id'))


class PostCommentView(BaseModelViewSet):
    queryset = PostComment.objects.all()
    serializer_class = PostCommentSerializer
    lookup_field = 'pk'


class PostImagesView(BaseModelViewSet):
    serializer_class = PostImageSerializer

    def get_queryset(self) -> QuerySet:
        return PostImage.objects.filter(post_id=self.kwargs.get('post_id'))
