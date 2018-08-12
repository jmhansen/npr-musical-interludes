import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from django.conf import settings

from songs.models import Artist, Song

# token = util.prompt_for_user_token(client_id=settings.SPOTIFY_CLIENT_ID)
client_credentials_manager = SpotifyClientCredentials(client_id=settings.SPOTIFY_CLIENT_ID, client_secret=settings.SPOTIFY_CLIENT_SECRET)
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def get_artist_thumbnail(artist_pk):
    artist = Artist.objects.get(pk=artist_pk)
    r = spotify.search(q='artist:' + artist.name, limit=1, type='artist')

    if len(r['artists']['items']) > 0:
        artist_dict = r['artists']['items'][0]
        if artist_dict['images'] and (len(artist_dict['images']) > 0):
            artist.thumbnail = artist_dict['images'][-1]['url']
            artist.save()


def get_song_preview(song_pk):
    song = Song.objects.get(pk=song_pk)
    r = spotify.search(q='track:' + song.name + ' ' + 'artist:' + song.artist.name, limit=1, type='track')
    if (len(r['tracks']['items']) > 0) and (r['tracks']['items'][0]['preview_url']):
        track_dict = r['tracks']['items'][0]
        song.preview = track_dict['preview_url']
        song.save()


# example response (with 2 results)

'''
Sample response for searching by track plus artist

{u'tracks': {
    u'href': u'https://api.spotify.com/v1/search?query=track%3ASo+Much+for+So+Little+artist%3AKaki+King&offset=0&limit=10&type=track',
    u'items': [{u'album': {u'album_type': u'album',
                           u'available_markets': [u'US'],
                           u'external_urls': {u'spotify': u'https://open.spotify.com/album/1RttIPWMaIgilxxWAsNEfN'},
                           u'href': u'https://api.spotify.com/v1/albums/1RttIPWMaIgilxxWAsNEfN',
                           u'id': u'1RttIPWMaIgilxxWAsNEfN',
                           u'images': [{u'height': 640,
                                        u'url': u'https://i.scdn.co/image/3b7438a6b6bb283a212defb6ebd765d981b65307',
                                        u'width': 640},
                                       {u'height': 300,
                                        u'url': u'https://i.scdn.co/image/65fbca0267dfd405cebf47a17a47d515b491f4c6',
                                        u'width': 300},
                                       {u'height': 64,
                                        u'url': u'https://i.scdn.co/image/b799e58e27060205636a52bb40f76a38b206c199',
                                        u'width': 64}],
                           u'name': u'Dreaming Of Revenge',
                           u'type': u'album',
                           u'uri': u'spotify:album:1RttIPWMaIgilxxWAsNEfN'},
                u'artists': [{u'external_urls': {u'spotify': u'https://open.spotify.com/artist/1s2pki7lATUaBOL76E3vCV'},
                              u'href': u'https://api.spotify.com/v1/artists/1s2pki7lATUaBOL76E3vCV',
                              u'id': u'1s2pki7lATUaBOL76E3vCV',
                              u'name': u'Kaki King',
                              u'type': u'artist',
                              u'uri': u'spotify:artist:1s2pki7lATUaBOL76E3vCV'}],
                u'available_markets': [u'US'],
                u'disc_number': 1,
                u'duration_ms': 212360,
                u'explicit': False,
                u'external_ids': {u'isrc': u'USVR40800407'},
                u'external_urls': {u'spotify': u'https://open.spotify.com/track/50fnNIHYwe5jHvMukAU7GS'},
                u'href': u'https://api.spotify.com/v1/tracks/50fnNIHYwe5jHvMukAU7GS',
                u'id': u'50fnNIHYwe5jHvMukAU7GS',
                u'name': u'So Much for So Little',
                u'popularity': 15,
                u'preview_url': u'https://p.scdn.co/mp3-preview/185cec24d5af3f86315ef9b0a5ff3dac6fca7a87',
                u'track_number': 7,
                u'type': u'track',
                u'uri': u'spotify:track:50fnNIHYwe5jHvMukAU7GS'},
               {u'album': {u'album_type': u'album',
                           u'available_markets': [u'AR',
                                                  u'ID'],
                           u'external_urls': {u'spotify': u'https://open.spotify.com/album/04npA91CxIHbYiMUDSJwYl'},
                           u'href': u'https://api.spotify.com/v1/albums/04npA91CxIHbYiMUDSJwYl',
                           u'id': u'04npA91CxIHbYiMUDSJwYl',
                           u'images': [{u'height': 640,
                                        u'url': u'https://i.scdn.co/image/81957e86fb24be41a47e0979930f07c4da09d6ee',
                                        u'width': 640},
                                       {u'height': 300,
                                        u'url': u'https://i.scdn.co/image/8b7445c2a7d4bd8246d625f57027aa4dc9dfa8be',
                                        u'width': 300},
                                       {u'height': 64,
                                        u'url': u'https://i.scdn.co/image/2a3ef9654cc2b3304ed193ec4f3cd0a6cf8ff038',
                                        u'width': 64}],
                           u'name': u'Everybody Glows: B-Sides & Rarities',
                           u'type': u'album',
                           u'uri': u'spotify:album:04npA91CxIHbYiMUDSJwYl'},
                u'artists': [{u'external_urls': {u'spotify': u'https://open.spotify.com/artist/1s2pki7lATUaBOL76E3vCV'},
                              u'href': u'https://api.spotify.com/v1/artists/1s2pki7lATUaBOL76E3vCV',
                              u'id': u'1s2pki7lATUaBOL76E3vCV',
                              u'name': u'Kaki King',
                              u'type': u'artist',
                              u'uri': u'spotify:artist:1s2pki7lATUaBOL76E3vCV'}],
                u'available_markets': [u'AR',
                                       u'ID'],
                u'disc_number': 1,
                u'duration_ms': 186252,
                u'explicit': False,
                u'external_ids': {u'isrc': u'TCACA1467726'},
                u'external_urls': {u'spotify': u'https://open.spotify.com/track/1B36AwqMYAj8SHKvPoHdj2'},
                u'href': u'https://api.spotify.com/v1/tracks/1B36AwqMYAj8SHKvPoHdj2',
                u'id': u'1B36AwqMYAj8SHKvPoHdj2',
                u'name': u'So Much for so Little (Demo)',
                u'popularity': 18,
                u'preview_url': u'https://p.scdn.co/mp3-preview/d1d7b1ffb7b572478d06498068518f738c47e968',
                u'track_number': 8,
                u'type': u'track',
                u'uri': u'spotify:track:1B36AwqMYAj8SHKvPoHdj2'}],
    u'limit': 10,
    u'next': None,
    u'offset': 0,
    u'previous': None,
    u'total': 2}}

---------------------------

Sample response for searching by artist alone

{u'artists': {u'href': u'https://api.spotify.com/v1/search?query=artist%3AKaki+King&offset=0&limit=1&type=artist',
              u'items': [{u'external_urls': {u'spotify': u'https://open.spotify.com/artist/1s2pki7lATUaBOL76E3vCV'},
                          u'followers': {u'href': None, u'total': 22330},
                          u'genres': [],
                          u'href': u'https://api.spotify.com/v1/artists/1s2pki7lATUaBOL76E3vCV',
                          u'id': u'1s2pki7lATUaBOL76E3vCV',
                          u'images': [{u'height': 1000,
                                       u'url': u'https://i.scdn.co/image/aa9bef47c2b29a578e0bdf9c9231ddfa8b25f985',
                                       u'width': 1000},
                                      {u'height': 640,
                                       u'url': u'https://i.scdn.co/image/3a6112807ae7e4d21993558d5c9e0ea6ce9834b4',
                                       u'width': 640},
                                      {u'height': 200,
                                       u'url': u'https://i.scdn.co/image/d7be4bd8e96d984d0530486db14dc4a389349a16',
                                       u'width': 200},
                                      {u'height': 64,
                                       u'url': u'https://i.scdn.co/image/6106135bd6528a76cbe19cc542b02958a74ee0d8',
                                       u'width': 64}],
                          u'name': u'Kaki King',
                          u'popularity': 54,
                          u'type': u'artist',
                          u'uri': u'spotify:artist:1s2pki7lATUaBOL76E3vCV'}],
              u'limit': 1,
              u'next': None,
              u'offset': 0,
              u'previous': None,
              u'total': 1}}
'''
