from rest_framework import serializers

from apps.my_workflows.models import Task, CycleTime, AcceptanceCriteria


class CycleTimeSerializer(serializers.ModelSerializer):

    class Meta:
        model = CycleTime
        fields = '__all__'


class AcceptanceCriteriaSerializer(serializers.ModelSerializer):

    class Meta:
        model = AcceptanceCriteria
        fields = '__all__'
        # read_only_fields = ['task']


class TaskSerializer(serializers.ModelSerializer):
    criterias = AcceptanceCriteriaSerializer(
        source='acceptance_criterias', many=True, read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'todo', 'description', 'criterias', 'status',
            'priority', 'date_created', 'date_updated', 'privacy', 'profile'
        ]
        read_only_fields = ['date_created']
