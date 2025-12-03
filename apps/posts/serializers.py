"""Serializers for apps/posts"""

from typing import Any
from rest_framework import serializers

from apps.posts.models import PostTag, Post, PostComment, PostImage


class CustomFieldsLastMixin:
    """Миксин который ставит кастомные поля в конец"""
    def get_field_names(self, declared_fields, info):
        fields = super().get_field_names(declared_fields, info)

        # Получаем все поля модели
        model = self.Meta.model
        model_fields = {f.name for f in model._meta.get_fields()}

        # Разделяем на поля модели и кастомные
        model_field_list = [f for f in fields if f in model_fields]
        custom_field_list = [f for f in fields if f not in model_fields]

        return model_field_list + custom_field_list


class GetPostObjectMixin:
    """
    Миксин для расширения функциональности
    """
    def get_post_object(self):
        """
        Получение объекта модели Post
        """
        view = self.context.get('view')
        if view and hasattr(view, 'kwargs'):
            post_id = view.kwargs.get('post_id')

        if post_id is None:
            raise serializers.ValidationError("Post ID not found")

        try:
            post = Post.objects.get(pk=post_id)
        except Post.DoesNotExist:
            post = None

        if post is None:
            raise serializers.ValidationError("Post object not found")

        return post


class PostTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostTag
        fields = '__all__'


class PostSerializer(CustomFieldsLastMixin, serializers.ModelSerializer):
    tag_names = serializers.ListField(
        child=serializers.CharField(max_length=20),
        # write_only=True,  # Только для записи
        required=False
    )

    class Meta:
        model = Post
        # fields = '__all__'
        exclude = ['tags']

    def create(self, validated_data: Any) -> Any:
        tag_names = validated_data.pop('tag_names', [])
        post = Post.objects.create(**validated_data)
        for name in tag_names:
            tag, _ = PostTag.objects.get_or_create(name=name)
            post.tags.add(tag)
        return post

    def update(self, instance, validated_data):
        tag_names = validated_data.pop('tag_names', None)

        # Обновляем остальные поля
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        # Обновляем теги если они переданы
        if tag_names is not None:
            instance.tags.clear()
            for tag_name in tag_names:
                tag, _ = PostTag.objects.get_or_create(name=tag_name)
                instance.tags.add(tag)

        return instance


class PostCommentsSerializer(GetPostObjectMixin, serializers.ModelSerializer):

    class Meta:
        model = PostComment
        # fields = '__all__'
        exclude = ['post']

    def create(self, validated_data: Any) -> Any:
        post = self.get_post_object()
        return PostComment.objects.create(post=post, **validated_data)


class PostCommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostComment
        # fields = '__all__'
        exclude = [
            'published_at', 'is_blocked',
            'is_deleted', 'parent', 'author',
            'post'
        ]


class PostImageSerializer(GetPostObjectMixin, serializers.ModelSerializer):

    class Meta:
        model = PostImage
        # fields = '__all__'
        exclude = ['post']

    def create(self, validated_data: Any) -> Any:
        post = self.get_post_object()
        return PostImage.objects.create(post=post, **validated_data)
