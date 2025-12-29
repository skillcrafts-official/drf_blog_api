from email.policy import default
from typing import Any
from attr import field
from django.db.models import Sum

from rest_framework import serializers

from apps.my_workflows.models import (
    Project, Tag, Task, CycleTime, AcceptanceCriteria, TimeEntry
)


class CycleTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleTime
        fields = '__all__'


class AcceptanceCriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcceptanceCriteria
        fields = '__all__'
        # read_only_fields = ['task']


class TimeEntrySerializer(serializers.ModelSerializer):
    # all_spents = serializers.SerializerMethodField()

    class Meta:
        model = TimeEntry
        fields = '__all__'

    # def get_all_spents(self):
    #     print(self.__dict__)

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.__dict__)
        representation.update(
            **TimeEntry.objects
            .filter(task=instance.task)
            .aggregate(all_spents=Sum('hours_spent'))
        )
        return representation


class TagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = ['name']

    def to_representation(self, instance: Any) -> str | Any:
        representation = super().to_representation(instance)
        return representation.get('name')


class UpdateTagSerializer(serializers.ModelSerializer):

    class Meta:
        model = Tag
        fields = '__all__'


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    criterias = AcceptanceCriteriaSerializer(
        source='acceptance_criterias', many=True, read_only=True
    )
    all_spents = TimeEntrySerializer(
        source='time_entries', many=True, read_only=True
    )
    tags = TagSerializer(source='task_tags', many=True, read_only=True)

    class Meta:
        model = Task
        # fields = [
        #     'id', 'todo', 'description', 'criterias', 'all_spents', 'status',
        #     'priority', 'date_created', 'date_updated', 'privacy', 'profile'
        # ]
        fields = '__all__'
        read_only_fields = ['date_created']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        # print(instance.__dict__)
        representation.update(
            **TimeEntry.objects
            .filter(task_id=instance.id)
            .aggregate(all_spents=Sum('hours_spent'))
        )
        return representation
