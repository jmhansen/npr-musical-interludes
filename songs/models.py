from __future__ import unicode_literals

from django.db import models


class Program(models.Model):
    """ Name of the NPR program or show"""
    name = models.CharField(max_length=50, unique=True)  # maybe make a choice field
    slug = models.SlugField(max_length=75)

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
    name = models.CharField(max_length=100, unique=True)

    def __unicode__(self):
        return self.name


class Song(models.Model):
    name = models.CharField(max_length=255)
    # Some songs do not have an artist listed
    artist = models.ForeignKey(Artist, related_name='songs', blank=True, null=True)

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

    def __unicode__(self):
        return u"{} - {} - {}".format(self.song.name, self.episode.program.name, self.order)
