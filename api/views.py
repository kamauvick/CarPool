# Create your views here.
import operator
import random
from functools import reduce

from django.db.models import Q
from django.http import JsonResponse
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import api_view, APIView
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from .models import Profile, User, Trip, Trip_Request
from .serializers import ProfileSerializer, UserSerializer, TripSerializer, TripRequestSerializer


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serialized_data = UserSerializer(users, many=True)
    params = {
        'users': serialized_data.data
    }
    return Response(params)


class ProfileView(ModelViewSet):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()

    def get_queryset(self):
        profile = self.request.user.profile
        if self.action in ['list', 'retrieve']:
            return [profile]

    def get_object(self):
        return self.request.user.profile


class TripsView(ModelViewSet):
    queryset = Trip.objects.all()
    serializer_class = TripSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    # filterset_fields = ['driver']
    search_fields = ['^destination']

    def get_queryset(self):
        queryset = super().get_queryset()
        _date = self.request.query_params.get('date', None)
        if _date:
            queryset = queryset.filter(date=_date)
        return queryset


class TripRequestView(ModelViewSet):
    queryset = Trip_Request.objects.all()
    serializer_class = TripRequestSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_fields = ["trip"]

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.action in ['list', 'retrieve']:
            p = self.request.user.profile
            # reduce(operator.or_, Q(trip__driver=p),Q(passenger=p))
            queryset = queryset.filter(reduce(operator.or_, (Q(trip__driver=p), Q(passenger=p))))
        return queryset


survey_questions = [
    "How was the overall experience?", "Would you use the app again?", "Would you suggest this trip to a colleague?"
]


class SendSurvey(APIView):
    def get(self, request):
        print(random.choice(survey_questions))
        params = {
            "question": random.choice(survey_questions),
        }
        return JsonResponse(params)
