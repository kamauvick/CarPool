# Create your views here.
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Profile, User, Trip
from .serializers import ProfileSerializer, UserSerializer, TripSerializer


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
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

    def post(self, request):
        profile = request.data
        serializer = ProfileSerializer(data=profile)
        if serializer.is_valid(raise_exception=True):
            saved_profile = serializer.save()
            profile_data = {
                'Success': f'Profile for {saved_profile.name}, created successfully'
            }
            return Response(profile_data)


class TripsView(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['^destination']

    def get_queryset(self):
        queryset = super().get_queryset()
        _date = self.request.query_params.get('date', None)
        if _date:
            queryset = queryset.filter(date=_date)
        return queryset


class RequestView(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    search_fields = ['^destination']

    def get_queryset(self):
        queryset = super().get_queryset()
        _date = self.request.query_params.get('date', None)
        if _date:
            queryset = queryset.filter(date=_date)
        return queryset
