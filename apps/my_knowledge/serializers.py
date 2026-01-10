"""Serializers for my_knowledge"""

from rest_framework import serializers

from apps.my_knowledge.models import MyKnowledge, Note


class NoteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Note
        fields = '__all__'


class MyKnowledgeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = MyKnowledge
        fields = '__all__'

    def get_children(self, obj):
        """Получаем дочерние элементы через MPTT"""
        # Используем предзагруженные children если есть
        if hasattr(obj, 'children_cache'):
            children = obj.children_cache
        else:
            children = obj.children.filter(is_deleted=False)

        if not children.exists():
            return []

        # Рекурсивно сериализуем детей
        serializer = self.__class__(children, many=True, context=self.context)
        return serializer.data
