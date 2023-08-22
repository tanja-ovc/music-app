from django.contrib import admin

from .models import Album, Artist, Track, TrackFromAlbum


@admin.register(Artist)
class ArtistAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Album)
class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name', 'artist', 'release_year')


@admin.register(Track)
class TrackAdmin(admin.ModelAdmin):
    list_display = ('id', 'name',)


@admin.register(TrackFromAlbum)
class TrackFromAlbumAdmin(admin.ModelAdmin):
    list_display = ('track', 'track_number', 'album')
