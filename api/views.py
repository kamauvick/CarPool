# Create your views here.
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Location, Profile, User, Trip_Request, Trip_Offers
from .serializers import LocationSerializer, ProfileSerializer, UserSerializer, TripOfferSerializer, \
    TripRequestSerializer


@api_view(['GET'])
def get_users(request):
    users = User.objects.all()
    serialized_data = UserSerializer(users, many=True)
    params = {
        'users': serialized_data.data
    }
    return Response(params)


class OfferView(APIView):
    def get(self, request):
        offers = Trip_Offers.objects.all()
        serialized_data = TripOfferSerializer(offers, many=True)
        params = {
            'offers': serialized_data.data
        }
        return Response(params)

    @classmethod
    def print_offers(cls):
        offers = Trip_Offers.objects.all()
        serialized_data = TripOfferSerializer(offers, many=True)
        params = {

            'offers': serialized_data.data
        }
        return Response(params)

    def post(self, request):
        offer = request.data
        serializer = TripOfferSerializer(data=offer)
        if serializer.is_valid(raise_exception=True):
            created_offer = serializer.save()
            offer_data = {
                'Success': f'An offer by {created_offer.driver} for {created_offer.destination} has been created',
            }
            return Response(offer_data)


class RequestView(APIView):
    def get(self, request):
        trip_requests = Trip_Request.objects.all()
        serialized_data = TripOfferSerializer(trip_requests, many=True)
        params = {
            "trip_requests": serialized_data.data
        }

        return JsonResponse(params, safe=False)

    def post(self, request):
        trip_request = request.data
        serializer = TripRequestSerializer(data=trip_request)
        if serializer.is_valid(raise_exception=True):
            created_request = serializer.save()
            request_data = {
                'Success': f'A request from {created_request.origin} to {created_request.destination} has been created',
                "matching_offers": OfferView.print_offers().data
            }

            print(request_data)
            return Response(request_data)


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


class LocationsList(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        locations = Location.objects.all()
        serialized_locations = LocationSerializer(locations, many=True)
        params = {
            'locations': serialized_locations.data
        }

        return Response(params)

    def post(self, request):
        location = self.request.data
        serializer = LocationSerializer(data=location)
        if serializer.is_valid(raise_exception=True):
            saved_location = serializer.save()
            print(saved_location)
            lacation_params = {
                'Success': f'Location {saved_location.name} saved successfully'
            }
            return Response(lacation_params)
