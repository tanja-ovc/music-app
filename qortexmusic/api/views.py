from rest_framework import viewsets

from music.models import Album, Artist, Track
from .serializers import (AlbumUpdateSerializer,
                          AlbumSerializer,
                          ArtistSerializer,
                          TrackSerializer,
                          TrackUpdateSerializer)


class ArtistViewSet(viewsets.ModelViewSet):
    queryset = Artist.objects.all()
    serializer_class = ArtistSerializer


class AlbumViewSet(viewsets.ModelViewSet):
    queryset = Album.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return AlbumUpdateSerializer
        return AlbumSerializer


class TrackViewSet(viewsets.ModelViewSet):
    queryset = Track.objects.all()

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return TrackUpdateSerializer
        return TrackSerializer
