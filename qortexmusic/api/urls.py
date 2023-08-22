from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import ArtistViewSet, AlbumViewSet, TrackViewSet

router = DefaultRouter()


router.register('artists', ArtistViewSet)
router.register('albums', AlbumViewSet)
router.register('tracks', TrackViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
