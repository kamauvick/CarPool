# Create your views here.
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location, Profile
from .serializers import LocationSerializer, ProfileSerializer, UserSerializer


class UserListView(APIView):
    def get(self, request):
        users = Profile.objects.all()
        serialized_data = UserSerializer(users, many=True)
        params = {
            'users': serialized_data.data
        }
        return Response(params)


class ProfileListView(APIView):
    def get(self, request):
        users = Profile.objects.all()
        serialized_data = ProfileSerializer(users, many=True)
        params = {
            'profiles': serialized_data.data
        }
        return Response(params)


class LocationsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        locations = Location.objects.all()
        serialized_locations = LocationSerializer(locations, many=True)
        params = {
            'locations': serialized_locations.data
        }

        return Response(params)
