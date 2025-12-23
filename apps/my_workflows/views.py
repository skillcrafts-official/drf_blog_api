from rest_framework import views
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied

from apps.profiles.models import Profile
from apps.privacy_settings.models import ProfilePrivacySettings
from apps.my_workflows.models import Task, CycleTime
from apps.my_workflows.serializers import TaskSerializer, CycleTimeSerializer

# from apps.accounts.permissions import AllowGuests


class TaskAPIView(views.APIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        profile = Profile.get_profile(user.pk)
        privacy = ProfilePrivacySettings.objects.get(profile=profile)
        tasks = Task.objects.filter(profile=profile)
        if user and user.is_authenticated and user in privacy.blacklist.all():
            raise PermissionDenied()
        serializer = self.serializer_class(
            tasks, context={'request': request}, many=True
        )
        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        data['profile'] = Profile.objects.get(user=user)
        serializer = self.serializer_class(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=201)
        return Response(data=serializer.errors, status=400)
