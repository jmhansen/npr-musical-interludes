from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView
from django.db.models import Count

from songs import models


class IndexView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['program_list'] = models.Program.objects.all()
        context['top_artists'] = (models.Artist.objects.exclude(hidden=True)
                                                       .annotate(interlude_count=Count('songs__interludes'))
                                                       .order_by('-interlude_count')[:10])
        context['top_songs'] = (models.Song.objects.annotate(interlude_count=Count('interludes'))
                                                   .order_by('-interlude_count')[:10])
        return context


class SongListTop25View(ListView):
    model = models.Song
    template_name = 'songs/songs_list_top_25.html'

    def get_queryset(self):
        return models.Song.objects.annotate(interlude_count=Count('interludes')).order_by('-interlude_count')[:25]


class ArtistListTop25View(ListView):
    model = models.Artist
    template_name = 'songs/artist_list_top_25.html'

    def get_queryset(self):
        return (models.Artist.objects.exclude(hidden=True)
                                     .annotate(interlude_count=Count('songs__interludes'))
                                     .order_by('-interlude_count')[:25])


class EpisodeDetailView(DetailView):
    model = models.Episode
    template_name = 'songs/episode_detail.html'

    def get_object(self, queryset=None):
        return models.Episode.objects.get(program__slug=self.kwargs['program_slug'], date=self.kwargs['episode_date'])

    def get_context_data(self, **kwargs):
        context = super(EpisodeDetailView, self).get_context_data(**kwargs)
        context['interlude_list'] = self.get_object().interludes.all()
        try:
            context['prev_episode'] = self.get_object().get_previous_by_date(program__name=self.get_object().program.name)
        except models.Episode.DoesNotExist:
            pass
        try:
            context['next_episode'] = self.get_object().get_next_by_date(program__name=self.get_object().program.name)
        except models.Episode.DoesNotExist:
            pass
        return context


class ArtistDetailView(DetailView):
    model = models.Artist
    template_name = 'songs/artist_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ArtistDetailView, self).get_context_data(**kwargs)
        context['artist_songs'] = (self.object.songs.all()
                                                    .annotate(interlude_count=Count('interludes'))
                                                    .order_by('-interlude_count'))
        return context
