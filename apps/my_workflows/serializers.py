from rest_framework import serializers

from apps.my_workflows.models import (
    Task, CycleTime, AcceptanceCriteria, TimeEntry
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

    class Meta:
        model = TimeEntry
        fields = '__all__'


class TaskSerializer(serializers.ModelSerializer):
    criterias = AcceptanceCriteriaSerializer(
        source='acceptance_criterias', many=True, read_only=True
    )
    hours_spents = TimeEntrySerializer(
        source='time_entries', many=True, read_only=True
    )

    class Meta:
        model = Task
        fields = [
            'id', 'todo', 'description', 'criterias', 'hours_spents', 'status',
            'priority', 'date_created', 'date_updated', 'privacy', 'profile'
        ]
        read_only_fields = ['date_created']
