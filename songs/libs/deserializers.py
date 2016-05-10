import datetime

# from songs import models
from ..models import Program, Episode, Artist, Song, Interlude


def create_from_dict(song_dict):
    # example dict:
    # {'date': u'April 20, 2016', 'program': u'Morning Edition', 'order': 19, 'song_title': u'Delphium',
    #  'artist': u'Aphex Twin'}

    # program = models.Program.objects.get_or_create(name=song_dict['program'])
    # episode = models.Episode.objects.get_or_create(program=program,
    #                                                date=datetime.datetime.strptime(song_dict['date'], '%B %d, %Y').date())
    # artist = models.Artist.objects.get_or_create(name=song_dict['artist'])
    # song = models.Song.objects.get_or_create(name=song_dict['song_title'], artist=artist)
    #
    # models.Interlude.objects.create(song=song, order=song_dict['order'], episode=episode)

    program, created = Program.objects.get_or_create(name=song_dict['program'])
    episode, created = Episode.objects.get_or_create(
        program=program,
        date=datetime.datetime.strptime(song_dict['date'], '%B %d, %Y').date()
    )
    artist, created = Artist.objects.get_or_create(name=song_dict['artist'])
    song, created = Song.objects.get_or_create(name=song_dict['song_title'], artist=artist)

    Interlude.objects.get_or_create(song=song, order=song_dict['order'], episode=episode)
