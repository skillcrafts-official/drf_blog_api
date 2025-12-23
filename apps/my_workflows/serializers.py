from rest_framework import serializers

from apps.my_workflows.models import Task, CycleTime


class TaskSerializer(serializers.ModelSerializer):

    class Meta:
        model = Task
        fields = [
            'id', 'todo', 'description', 'status',
            'priority', 'date_created', 'privacy', 'profile'
        ]
        read_only_fields = ['date_created']


class CycleTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleTime
        fields = '__all__'
