from django.urls import include, path
from rest_framework.routers import SimpleRouter
from .views import LocationsList, get_users, ProfileListView, OfferView,RequestView, TripsView


router = SimpleRouter()
router.register('trips',TripsView,base_name='trips-view' )

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),
    path('users/', get_users),
    path('profiles/', ProfileListView.as_view()),
    path('offers/', OfferView.as_view(), name='createtrip'),
    path('request/', RequestView.as_view(), name='requesttrip'),
    path('locations/', LocationsList.as_view(), name='locations'),
    path("", include(router.urls))
]

