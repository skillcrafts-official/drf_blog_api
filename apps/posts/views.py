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
    PostImageSerializer, PostCommentsSerializer
)
from apps.posts.models import (
    PostTag, Post, PostComment, PostImage
)
from apps.posts.filters import django_filters, PostFilters

from drf_spectacular.utils import (
    inline_serializer, extend_schema, extend_schema_view,
    OpenApiParameter
)


class BaseModelViewSet(ModelViewSet):
    # permission_classes = [IsAuthenticated]
    ...


class PostTagsView(BaseModelViewSet):
    queryset = PostTag.objects.all()
    serializer_class = PostTagSerializer

    # def get_queryset(self) -> QuerySet:
    #     return PostTag.objects.filter(post_id=self.kwargs.get('post_id'))


# class PostTagView(BaseModelViewSet):
#     queryset = PostTag.objects.all()
#     serializer_class = PostTagSerializer
#     lookup_field = 'pk'


class PostsView(BaseModelViewSet):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    filterset_class = PostFilters


class PostView(BaseModelViewSet):
    queryset = Post.objects.filter(is_deleted=False)
    serializer_class = PostSerializer
    lookup_field = 'pk'


class PostCommentsView(BaseModelViewSet):
    serializer_class = PostCommentsSerializer

    def get_queryset(self) -> QuerySet:
        return PostComment.objects.filter(
            post_id=self.kwargs.get('post_id'),
            is_deleted=False
        )


class PostCommentView(BaseModelViewSet):
    queryset = PostComment.objects.filter(is_deleted=False)
    serializer_class = PostCommentSerializer
    lookup_field = 'pk'


class PostImagesView(BaseModelViewSet):
    serializer_class = PostImageSerializer

    def get_queryset(self) -> QuerySet:
        return PostImage.objects.filter(post_id=self.kwargs.get('post_id'))
