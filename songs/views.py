from django.shortcuts import render
from django.views.generic import TemplateView, ListView
from django.db.models import Count

from songs import models


class IndexView(TemplateView):
    template_name = 'index.html'


class SongListTop25View(ListView):
    model = models.Song
    template_name = 'songs/songs_list_top_25.html'

    def get_queryset(self):
        return models.Song.objects.annotate(interlude_count=Count('interludes')).order_by('-interlude_count')[:25]
