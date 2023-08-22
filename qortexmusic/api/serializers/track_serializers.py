from rest_framework import serializers

from api.validators import (duplicates_validator,
                            track_is_listed_on_album_validator,
                            track_number_is_taken_validator)
from music.models import Album, Track, TrackFromAlbum


class AlbumAndTrackNumberSerializer(serializers.ModelSerializer):
    '''
    Предназначен для использования при получении/записи данных о песнях.
    Позволяет получить/записать названия альбомов, в которые включены песни,
    вместе с порядковыми номерами песен в этих альбомах.
    '''
    album = serializers.SlugRelatedField(
        queryset=Album.objects.all(), slug_field='name')

    class Meta:
        model = TrackFromAlbum
        fields = ('album', 'track_number')


class TrackSerializer(serializers.ModelSerializer):
    albums = AlbumAndTrackNumberSerializer(
        source='trackfromalbum_set', many=True)

    class Meta:
        model = Track
        fields = ('id', 'name', 'albums')

    def create(self, validated_data):
        albums_and_track_numbers = validated_data.pop('trackfromalbum_set')

        if len(albums_and_track_numbers) > 1:
            duplicates_validator(
                albums_and_track_numbers, 'album',
                'Нельзя добавить одну песню в альбом несколько раз.')

        track_obj = Track.objects.create(**validated_data)

        for album_and_track_number in albums_and_track_numbers:
            track_name = validated_data.get('name')
            album = album_and_track_number.get('album')
            track_number = album_and_track_number.get('track_number')

            track_is_listed_on_album_validator(track_name, album)
            track_number_is_taken_validator(track_number, album)

            TrackFromAlbum.objects.create(
                album=album,
                track=track_obj,
                track_number=track_number)

        return track_obj


class TrackUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Track
        fields = ('id', 'name')
