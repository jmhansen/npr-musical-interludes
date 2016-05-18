import requests, datetime
from bs4 import BeautifulSoup

from songs.models import Program


def get_songs_from_programs_page(url, program=None):
    # r = requests.get('http://www.npr.org/programs/morning-edition/')
    r = requests.get(url)

    if r.status_code == 200:

        soup = BeautifulSoup(r.text, 'lxml')
        show_date = soup.find(class_='date').text

        if program:
            show_title = program.name
        else:
            show_title = soup.title.text.split(' : ')[0]
            show_title = show_title.split(' for ')[0]  # Should return u'Morning Edition'

        songs = soup.find_all(class_='song-meta-wrap')

        song_list = []

        for song in songs:
            # solve for empty song_title or artist tag
            if song.find(class_='song-meta-title'):
                song_title = song.find(class_='song-meta-title').text.strip()
            else:
                song_title = ''

            if song.find(class_='song-meta-artist'):
                artist = song.find(class_='song-meta-artist').text.strip()
            else:
                artist = ''

            if song_title and artist:
                song_dict = {
                    'song_title': song_title,
                    'artist': artist,
                    'order': songs.index(song),
                    'program': show_title,
                    'date': show_date
                }
                song_list.append(song_dict)

        print "{} songs in song_list".format(len(song_list))
        return song_list

    else:
        print u"Status code {} for url {}".format(r.status_code, url)


def crawl_for_song_lists(url_list, program=None):
    super_song_list = []
    for url in url_list:
        print "starting {}".format(url)
        super_song_list.extend(get_songs_from_programs_page(url=url, program=program))
        print "finished {}".format(url)

    return super_song_list


# def get_data_from_latest_npr_episode(program_pk):
#     program = Program.objects.get(pk=program_pk)
#
#     r = requests.get(program.href)
#
#     if r.status_code == 200:
#         soup = BeautifulSoup(r.text, 'lxml')
#         show_date = soup.find(class_='date').text
#         prev_link = soup.find(class_='prev').next_element['href']
#
#         show_date_object = datetime.datetime.strptime(show_date, '%B %d, %Y').date()
#
#         if show_date_object > program.date_latest_episode:

