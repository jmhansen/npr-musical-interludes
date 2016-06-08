from __future__ import unicode_literals

from django.db import models
from django.db.models import Count


class Program(models.Model):
    """ Name of the NPR program or show"""
    name = models.CharField(max_length=50, unique=True)  # maybe make a choice field
    slug = models.SlugField(max_length=75)
    href = models.URLField(blank=True)

    def __unicode__(self):
        return self.name

    @property
    def date_latest_episode(self):
        return self.episodes.latest().date


class Episode(models.Model):
    """ Specific airing of a program, unique by date"""
    program = models.ForeignKey(Program, related_name='episodes')
    date = models.DateField()

    class Meta:
        unique_together = ('program', 'date')
        get_latest_by = 'date'


class Artist(models.Model):
    name = models.CharField(max_length=125, unique=True)
    slug = models.SlugField(max_length=150)
    thumbnail = models.URLField(blank=True)

    # for 'Various Artists', 'NA', and others that should not be displayed in lists of artists
    hidden = models.BooleanField(default=False)

    def __unicode__(self):
        return self.name

    @property
    def num_songs(self):
        return self.songs.count()

    @property
    def num_interludes(self):
        return Interlude.objects.filter(song__artist=self).count()

    @property
    def earliest_episode(self):
        return Episode.objects.filter(interludes__song__artist=self).earliest('date')

    @property
    def latest_episode(self):
        return Episode.objects.filter(interludes__song__artist=self).latest('date')


class Song(models.Model):
    name = models.CharField(max_length=255)
    # Some songs do not have an artist listed
    artist = models.ForeignKey(Artist, related_name='songs', blank=True, null=True)
    preview = models.URLField(blank=True)

    class Meta:
        unique_together = ('name', 'artist')

    def __unicode__(self):
        return self.name

    @property
    def num_interludes(self):
        return self.interludes.count()

    @property
    def date_last_played(self):
        return self.interludes.latest().episode.date


class Interlude(models.Model):
    """ The clip or instance of a song used in an interlude. """
    song = models.ForeignKey(Song, related_name='interludes')
    order = models.PositiveSmallIntegerField()
    episode = models.ForeignKey(Episode, related_name='interludes')

    class Meta:
        unique_together = ('song', 'order', 'episode')
        get_latest_by = 'episode__date'
        ordering = ['order']

    def __unicode__(self):
        return u"{} - {} - {}".format(self.song.name, self.episode.program.name, self.order)
