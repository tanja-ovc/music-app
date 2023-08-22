from rest_framework import serializers

from api.validators import duplicates_validator
from music.models import Album, Artist, Track, TrackFromAlbum


class TrackAndTrackNumberSerializer(serializers.ModelSerializer):
    '''
    Предназначен для использования при получении данных об альбомах.
    Позволяет получить названия песен, включённых в альбомы, вместе
    с их порядковыми номерами в этих альбомах.
    '''
    track = serializers.CharField()

    class Meta:
        model = TrackFromAlbum
        fields = ('track_number', 'track')


class AlbumSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(), slug_field='name')
    tracks = TrackAndTrackNumberSerializer(
        source='trackfromalbum_set', many=True, required=False)

    class Meta:
        model = Album
        fields = ('id', 'name', 'artist', 'release_year', 'tracks')

    def create(self, validated_data):
        if 'tracks' not in self.initial_data:
            album_obj = Album.objects.create(**validated_data)
            return album_obj

        tracks_and_track_numbers = validated_data.pop('trackfromalbum_set')
        if len(tracks_and_track_numbers) > 1:
            duplicates_validator(
                tracks_and_track_numbers, 'track',
                'Нельзя дублировать названия песен в альбоме.')
            duplicates_validator(
                tracks_and_track_numbers, 'track_number',
                'Нельзя дублировать номера песен в альбоме.')

        album_obj = Album.objects.create(**validated_data)

        for track_and_track_number in tracks_and_track_numbers:
            track_name = track_and_track_number.get('track')
            track_number = track_and_track_number.get('track_number')

            track_obj = Track.objects.create(name=track_name)
            TrackFromAlbum.objects.create(
                album=album_obj,
                track=track_obj,
                track_number=track_number)

        return album_obj


class AlbumUpdateSerializer(serializers.ModelSerializer):
    artist = serializers.SlugRelatedField(
        queryset=Artist.objects.all(), slug_field='name')

    class Meta:
        model = Album
        fields = ('id', 'name', 'artist', 'release_year')
