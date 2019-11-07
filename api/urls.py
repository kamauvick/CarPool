from django.urls import include, path

from .views import LocationsList, UserListView, ProfileListView

urlpatterns = [
    path('auth/', include('rest_auth.urls')),
    path('auth/register/', include('rest_auth.registration.urls')),
    path('users/', UserListView.as_view()),
    path('profiles/', ProfileListView.as_view()),
    path('locations/', LocationsList.as_view(), name='locations')
]
