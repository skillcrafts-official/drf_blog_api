"""Serializers for my_knowledge"""

from rest_framework import serializers

from apps.my_knowledge.models import MyKnowledge, Topic


class TopicSerializer(serializers.ModelSerializer):

    class Meta:
        model = Topic
        fields = '__all__'


class MyKnowledgeSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyKnowledge
        fields = '__all__'
