import datetime as dt

from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models


class Artist(models.Model):
    name = models.CharField(
        'имя исполнителя/название группы', max_length=70, unique=True)

    class Meta:
        verbose_name = 'исполнитель'
        verbose_name_plural = 'исполнители'

    def __str__(self):
        return f'{self.name}'


class Album(models.Model):
    name = models.CharField('название альбома', max_length=70, unique=True)
    artist = models.ForeignKey(
        Artist, on_delete=models.CASCADE, verbose_name='исполнитель',
        related_name='albums')
    release_year = models.PositiveSmallIntegerField(
        'год выпуска', validators=[
            MinValueValidator(1860,
                              'Первая в мире аудиозапись сделана в 1860 году. '
                              'В нашем каталоге не может быть альбомов, '
                              'выпущенных до этого времени!'),
            MaxValueValidator(dt.datetime.utcnow().year + 1,
                              'В наш каталог мы сможем добавить только уже '
                              'вышедший альбом, либо альбом, выпуск которого '
                              'назначен на этот или следующий год.')
        ]
    )

    class Meta:
        verbose_name = 'альбом'
        verbose_name_plural = 'альбомы'

    def __str__(self):
        return f'{self.name}'


class TrackFromAlbum(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE)
    track = models.ForeignKey('Track', on_delete=models.CASCADE)
    track_number = models.SmallIntegerField(
        'номер песни/трека в альбоме', validators=[MinValueValidator(
            1, 'Номер песни/трека не может быть меньше 1.')])

    class Meta:
        verbose_name = 'номер песни/трека в альбоме'
        verbose_name_plural = 'номера песен/треков в альбомах'
        unique_together = ('album', 'track', 'track_number')

    def __str__(self):
        return f'{self.track_number} - {self.track}'


class Track(models.Model):
    name = models.CharField('название песни/трека', max_length=70)
    albums = models.ManyToManyField(
        Album, through=TrackFromAlbum, verbose_name='из альбома',
        related_name='tracks')

    class Meta:
        verbose_name = 'песня/трек'
        verbose_name_plural = 'песни/треки'

    def __str__(self):
        return f'{self.name}'
