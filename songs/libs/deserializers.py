import datetime

from django.utils.text import slugify

from spotipy.client import SpotifyException

from ..models import Program, Episode, Artist, Song, Interlude
from .spotify_api_utils import get_artist_thumbnail, get_song_preview


def create_from_dict(song_dict):
    # example dict:
    # {'date': u'April 20, 2016', 'program': u'Morning Edition', 'order': 19, 'song_title': u'Delphium',
    #  'artist': u'Aphex Twin'}

    artist_name = song_dict['artist']
    song_name = song_dict['song_title']

    # check for empty artist and song keys
    if not (artist_name and song_name):
        return "skipping empty dictionary"

    # Check and reconcile known variations
    various = ['various artists', 'various']
    unknown = ['unknown artist', 'unknown']

    if artist_name.lower() in various:
        artist_name = 'Various Artists'

    if artist_name.lower() in unknown:
        artist_name = 'unknown'

    # Check for empty artist key
    if not artist_name:
        artist_name = 'no artist listed'

    # Check for all caps and clean
    if artist_name.isupper():
        artist_name = artist_name.title()

    if song_name.isupper():
        song_name = song_name.title()

    # truncate artist names that violate max length on field
    if len(artist_name) > 125:
        artist_name = artist_name[:125]

    # get or create objects
    program, created = Program.objects.get_or_create(name=song_dict['program'], slug=slugify(song_dict['program']))
    episode, created = Episode.objects.get_or_create(
        program=program, date=datetime.datetime.strptime(song_dict['date'], '%B %d, %Y').date())
    artist, created = Artist.objects.get_or_create(name=artist_name, slug=slugify(artist_name))
    if created or not artist.thumbnail:
        try:
            get_artist_thumbnail(artist.pk)
        except SpotifyException:
            pass
    song, created = Song.objects.get_or_create(name=song_name, artist=artist)
    if created or not song.preview:
        try:
            get_song_preview(song.pk)
        except SpotifyException:
            pass
    Interlude.objects.get_or_create(song=song, order=song_dict['order'], episode=episode)


def create_from_list(list_of_dicts):

    for song_dict in list_of_dicts:
        _index = list_of_dicts.index(song_dict)
        print "Starting index {} of {}".format(_index, (len(list_of_dicts) - 1))
        create_from_dict(song_dict=song_dict)
        print "Finished index {}".format(_index)
