from django.contrib import admin

from .models import Program, Episode, Artist, Song, Interlude


admin.site.register(Program)
admin.site.register(Episode)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(Interlude)
