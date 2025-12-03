from django.urls import path
from apps.posts.views import (
    PostTagsView,  # PostTagView,
    PostView, PostsView,
    PostCommentsView, PostCommentView,
    PostImagesView,
)


urlpatterns = [
    path(
        'tags/', PostTagsView.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='get_post_tag_list_or_create_post_tag'
    ),
    path(
        '', PostsView.as_view({'get': 'list', 'post': 'create'}),
        name='get_post_list_or_create_one_post'
    ),
    path(
        '<int:pk>/', PostView.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }),
        name='get_or_update_one_post'
    ),
    path(
        '<int:post_id>/comments/', PostCommentsView.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='get_post_comments_or_create_post_comment'
    ),
    path(
        '<int:post_id>/comments/<int:pk>/', PostCommentView.as_view({
            'get': 'retrieve', 'put': 'update', 'delete': 'destroy'
        }),
        name='get_or_update_or_delete_one_post_comment'
    ),
    path(
        '<int:post_id>/images/', PostImagesView.as_view({
            'get': 'list', 'post': 'create'
        }),
        name='get_post_images_or_create_post_image'
    )
]
