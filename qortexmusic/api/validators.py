from rest_framework import serializers

from music.models import Album, TrackFromAlbum


def track_is_listed_on_album_validator(track_name, album):
    track_is_listed_on_album = TrackFromAlbum.objects.filter(
        track__name=track_name,
        album=Album.objects.filter(name=album.name).first()
        ).exists()
    if track_is_listed_on_album:
        raise serializers.ValidationError(
            'В указанный альбом уже добавлена такая песня.')


def track_number_is_taken_validator(track_number, album):
    track_number_is_taken = TrackFromAlbum.objects.filter(
        album=Album.objects.filter(name=album.name).first(),
        track_number=track_number
    ).exists()
    if track_number_is_taken:
        raise serializers.ValidationError(
            'В указанный альбом уже добавлена песня под таким '
            'номером.')


def duplicates_validator(objs, get_key: str, err_msg: str):
    values_list = [obj.get(get_key) for obj in objs]
    if len(values_list) > len(set(values_list)):
        raise serializers.ValidationError(err_msg)
