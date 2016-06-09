from django.test import TestCase, Client
from django.core.urlresolvers import reverse

from model_mommy import mommy

from songs.models import Program, Episode, Artist, Song, Interlude


class SongsViewsBaseTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.program = mommy.make(Program, name='All Things Considered')
        cls.episode = mommy.make(Episode, program=cls.program)
        cls.artist = mommy.make(Artist, name='Test Artist')
        cls.song = mommy.make(Song, name='Test Song', artist=cls.artist)
        cls.interlude = mommy.make(Interlude, song=cls.song)


class IndexViewTests(SongsViewsBaseTestCase):

    def test_for_http_200_response(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)


class SongListTop25ViewTests(SongsViewsBaseTestCase):

    def test_for_http_200_response(self):
        response = self.client.get(reverse('song_list_top_25'))
        self.assertEqual(response.status_code, 200)


class ArtistListTop25ViewTests(SongsViewsBaseTestCase):

    def test_for_http_200_response(self):
        response = self.client.get(reverse('artist_list_top_25'))
        self.assertEqual(response.status_code, 200)


class EpisodeDetailViewTests(SongsViewsBaseTestCase):

    def test_for_http_200_response(self):
        response = self.client.get(reverse('episode_detail', kwargs={'program_slug': self.program.slug,
                                                                     'episode_date': self.episode.date}))
        self.assertEqual(response.status_code, 200)


class ArtistDetailViewTests(SongsViewsBaseTestCase):

    def test_for_http_200_response(self):
        response = self.client.get(reverse('artist_detail', kwargs={'slug': self.artist.slug}))
        self.assertEqual(response.status_code, 200)


class ProgramDetailViewTests(SongsViewsBaseTestCase):

    def test_for_http_200_response(self):
        response = self.client.get(reverse('program_detail', kwargs={'slug': self.program.slug}))
        self.assertEqual(response.status_code, 200)
