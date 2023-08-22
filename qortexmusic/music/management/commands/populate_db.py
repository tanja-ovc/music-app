import csv
import os

from django.conf import settings
from django.core.management.base import BaseCommand

from music.models import (
    Album,
    Artist,
    TrackFromAlbum,
    Track,
)

MODEL_NAME_FILE = {
    'album': (Album, 'album.csv'),
    'artist': (Artist, 'artist.csv'),
    'track': (Track, 'track.csv'),
    'track_from_album': (TrackFromAlbum, 'track_from_album.csv'),
}


class Command(BaseCommand):
    help = 'Load data from a csv file to the corresponding db table'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    @staticmethod
    def get_csv_file(filename):
        return os.path.join(
            settings.BASE_DIR, 'music', 'csv_data', filename
        )

    @staticmethod
    def clear_model(model):
        model.objects.all().delete()

    def print_to_terminal(self, message):
        self.stdout.write(self.style.SUCCESS(message))

    def load_model(self, model_name, field_names):
        model, file_path = MODEL_NAME_FILE.get(model_name)
        with open(self.get_csv_file(file_path)) as file:
            reader = csv.reader(file, delimiter=',')
            self.clear_model(model)
            line = 0
            for row in reader:
                if row != '' and line > 0:
                    params = dict(zip(field_names, row))
                    _, created = model.objects.get_or_create(**params)
                line += 1
        self.print_to_terminal(
            f'{line - 1} objects added to "{model_name}" table'
        )

    def load_artist(self):
        self.load_model(
            'artist',
            ('id', 'name')
        )

    def load_album(self):
        self.load_model(
            'album',
            ('id', 'name', 'artist_id', 'release_year')
        )

    def load_track(self):
        self.load_model(
            'track',
            ('id', 'name')
        )

    def load_track_from_album(self):
        self.load_model(
            'track_from_album',
            ('id', 'album_id', 'track_id', 'track_number')
        )

    def handle(self, *args, **kwargs):
        self.load_artist()
        self.load_album()
        self.load_track()
        self.load_track_from_album()
