import datetime

from django.utils.text import slugify
# from songs import models
from ..models import Program, Episode, Artist, Song, Interlude


def create_from_dict(song_dict):
    # example dict:
    # {'date': u'April 20, 2016', 'program': u'Morning Edition', 'order': 19, 'song_title': u'Delphium',
    #  'artist': u'Aphex Twin'}

    various = ['Various Artists', 'Various', 'VARIOUS ARTISTS', 'VARIOUS', 'various']

    if song_dict['artist'] in various:
        song_dict['artist'] = 'Various Artists'

    program, created = Program.objects.get_or_create(name=song_dict['program'])
    episode, created = Episode.objects.get_or_create(
        program=program,
        date=datetime.datetime.strptime(song_dict['date'], '%B %d, %Y').date()
    )
    if len(song_dict['artist']) > 100:
        song_dict['artist'] = song_dict['artist'][:99]
    artist, created = Artist.objects.get_or_create(name=song_dict['artist'], slug=slugify(song_dict['artist']))
    song, created = Song.objects.get_or_create(name=song_dict['song_title'], artist=artist)

    Interlude.objects.get_or_create(song=song, order=song_dict['order'], episode=episode)
