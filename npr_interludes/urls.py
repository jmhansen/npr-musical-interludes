"""npr_interludes URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from songs import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.IndexView.as_view(), name='home'),
    url(r'^songs/top-25/$', views.SongListTop25View.as_view(), name='song_list_top_25'),
    url(r'^artists/top-25/$', views.ArtistListTop25View.as_view(), name='artist_list_top_25'),
    url(r'^episodes/(?P<program_slug>[\w-]+)/(?P<episode_date>[0-9-]+)/$',
        views.EpisodeDetailView.as_view(), name='episode_detail')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
