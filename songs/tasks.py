from __future__ import absolute_import

from libs.utils.compile_npr_links import get_latest_npr_links
from libs.utils.html_parsers import crawl_for_song_lists
from songs.libs.deserializers import create_from_list

from songs.models import Program


def update_npr_program(program_pk):
    program = Program.objects.get(pk=program_pk)
    links = get_latest_npr_links(program.href, program.pk)
    song_list = crawl_for_song_lists(links, program=program)
    create_from_list(song_list)


def update_multiple_npr_programs(program_pks):

    for pk in program_pks:
        update_npr_program(pk)
