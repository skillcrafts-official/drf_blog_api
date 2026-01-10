"""The urls routing for app my_knowledge"""

from django.urls import path

from apps.my_knowledge.viewsets import NoteViewSet, MyKnowledgeViewSet


urlpatterns = [
    path(
        '', MyKnowledgeViewSet.as_view({'get': 'list', 'post': 'create'}),
        name='get_notes_with_privacies_or_create_one'
    ),
    path(
        'for-user/<int:user_id>/',
        MyKnowledgeViewSet.as_view({'get': 'get_user_note_list'}),
        name='get_notes_only_user_id'
    ),
    path(
        'topics/<int:topic_id>/',
        MyKnowledgeViewSet.as_view({
            'get': 'retrieve', 'patch': 'partial_update', 'delete': 'destroy'
        }), name='get_one_topic_or_update_or_delete'
    ),
    path(
        'notes/<int:note_id>/',
        NoteViewSet.as_view({
            'get': 'retrieve', 'patch': 'partial_update'
        }), name='get_or_update_one_note'
    ),
    # path(
    #     'topics/', TopicViewSet.as_view({'get': 'list', 'post': 'create'}),
    #     name='get_all_topics_or_create_one'
    # )
]
