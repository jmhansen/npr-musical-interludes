import requests, datetime
from bs4 import BeautifulSoup

from songs.models import Program


def get_npr_links(starting_url):
    links = []
    r = requests.get(starting_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        # find link to previous show
        prev = soup.find(class_='prev')
        links.append(prev.next_element['href'])
        print(len(links))
        get_npr_links(links[-1])
    else:
        print("Added {} links".format(len(links)))

    return links


def get_npr_links_from_archive_page(archive_url):
    r = requests.get(archive_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        shows_raw = soup.find_all(class_='program-show__title')
        show_urls = [show.find('a')['href'] for show in shows_raw]
        return show_urls


def get_latest_npr_links(starting_url, program_pk, initial=True, _list=None):
    """ Check for program episodes not already entered in database """
    if initial:
        latest_links = []
    else:
        latest_links = _list
    program = Program.objects.get(pk=program_pk)
    r = requests.get(starting_url)
    if r.status_code == 200:
        print("Starting url: {}".format(starting_url))
        soup = BeautifulSoup(r.text, 'lxml')

        show_date = soup.find(class_='date').text
        prev_url = soup.find(class_='prev').next_element['href']

        show_date_object = datetime.datetime.strptime(show_date, '%B %d, %Y').date()

        if show_date_object > program.date_latest_episode:
            latest_links.append(starting_url)
            print("Appended url to list")
            get_latest_npr_links(starting_url=prev_url, program_pk=program_pk, initial=False, _list=latest_links)

        return latest_links
