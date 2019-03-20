from __future__ import absolute_import
from datetime import datetime

from libs.utils.compile_npr_links import get_npr_links_from_archive_page
from libs.utils.html_parsers import crawl_for_song_lists
from songs.libs.deserializers import create_from_list

from songs.models import Program, Episode


def add_songs_to_database(program_pk):
    program = Program.objects.get(pk=program_pk)
    links = get_npr_links_from_archive_page(program.archive_href)
    new_links = []
    for link in links:
        # '2018-07-23'
        date_string = link.split('showDate=')[-1]
        dt = datetime.strptime(date_string, '%Y-%m-%d')
        
        # Check if episode is already in database
        if not Episode.objects.filter(program=program, date=dt.date()).exists():
            new_links.append(link)

    song_list = crawl_for_song_lists(new_links, program=program)
    create_from_list(song_list)
    

def update_multiple_npr_programs(program_pks):

    for pk in program_pks:
        update_npr_program(pk)
