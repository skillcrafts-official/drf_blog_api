from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, status
from rest_framework.permissions import IsAuthenticated
# from drf_spectacular.utils import extend_schema_view, extend_schema

from apps.profiles.models import Profile
from apps.profiles.serializers import ProfileSerializer, SelfProfileSerializer


class ProfilesView(APIView):
    serializer_class = ProfileSerializer

    def get(self, request, *args, **kwargs):
        return Response()


class UserProfileView(ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    lookup_field = 'pk'


class SelfUserProfileView(APIView):
    serializer_class = SelfProfileSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        try:
            # profile = Profile.objects.get(pk=user.id)
            profile = request.user.profile
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
            serializer = self.serializer_class(profile, data=data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(
                    data=serializer.data, status=200
                )
        except Profile.DoesNotExist as e:
            return Response(
                data={
                    'detail': str(e)
                }, status=status.HTTP_404_NOT_FOUND
            )
        return Response(
            data=serializer.errors, status=status.HTTP_400_BAD_REQUEST
        )

    def delete(self, request, *args, **kwargs):
        user = request.user
        user.is_active = False
        user.save()
        response = Response(status=status.HTTP_204_NO_CONTENT)
        response['X-Message'] = 'User has been deleted!'
        return response
