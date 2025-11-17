from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, status
from rest_framework.permissions import IsAuthenticated
# from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer, ProfileImageSerializer


class ProfilesView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return Response()


class UserProfileView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            # profile = Profile.objects.get(pk=user.id)
            profile = request.user.profiles
        except Profile.DoesNotExist:
            profile = None
        if profile is None:
            raise NotFound(
                detail={
                    "message": "Profile not found. Please create them"
                }, code=status.HTTP_404_NOT_FOUND
            )
        serializer = self.serializer_class(profile)
        return Response(data=serializer.data, status=200)

    def post(self, request, *args, **kwargs):
        user = request.user
        data = request.data
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            profile = None

        if profile:
            serializer = self.serializer_class(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=serializer.data, status=200
                )
        if not profile:
            data['user'] = user.id
            serializer = self.serializer_class(data=data)
            if serializer.is_valid():
                data = serializer.validated_data
                data['user'] = user
                profile = Profile.objects.create(**data)
                serializer = self.serializer_class(profile)
                return Response(data=serializer.data, status=201)
        return Response(data=serializer.errors, status=404)

    def put(self, request, *args, **kwargs):
        ...

    def delete(self, request, *args, **kwargs):
        ...
