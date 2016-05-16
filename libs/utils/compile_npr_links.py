import requests
from bs4 import BeautifulSoup

links = []

def get_npr_links(starting_url):
    r = requests.get(starting_url)
    if r.status_code == 200:
        soup = BeautifulSoup(r.text, 'lxml')
        # find link to previous show
        prev = soup.find(class_='prev')
        links.append(prev.next_element['href'])
        print len(links)
        get_npr_links(links[-1])
    else:
        print "Added {} links".format(len(links))

    return links

if __name__ == "__main__":
    import sys
    get_npr_links(sys.argv[1])

