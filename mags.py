
import re, sys, csv
import requests
from bs4 import BeautifulSoup


URL = "https://magazinescanada.ca/member-directory/"

class Magazine(object):
    def __init__(self, name, street, city, prov, website):
        self.name = name
        self.street = street
        self.city = city
        self.prov = prov
        self.website = website

    def __str__(self):
        return "{0}\n{1}\n{2}\n{3}\n{4}\n".format(self.name, self.street, \
            self.city, self.prov, self.website)

def get_html(url):
    r = requests.get(url)
    if r.status_code == requests.codes.ok:
        page = r.text
        print("HTTP Status: 200")
        #print(len(page))
    return page

def parse_canmags(html):

    def split_addr(mag):
        components = mag.p.get_text().split('\n')
        # split city / province
        lst = components[1].split(',')
        components.pop(1)
        components.insert(1, lst[0])
        components.insert(2, lst[-1])
        return [x.strip() for x in components]

    soup = BeautifulSoup(html, 'lxml')
    mags = soup.find_all('div', class_=re.compile('^member'))
    print("Magazines found: {0}".format(len(mags)))

    # parse each individual magazine
    all_mags = []
    for mag in mags:
        name = mag.h2.string
        addr = split_addr(mag)
        street = addr[0]
        city = addr[1]
        prov = addr[2]
        website = mag.a.get('href')
        magazine = Magazine(name, street, city, prov, website)
        all_mags.append(magazine)
    return all_mags

def write_to_csv(obj):

    return

if __name__ == "__main__":

    # fetch the page
    page = get_html(URL)

    # parse the page
    list_of_mags = parse_canmags(page)
    print(len(list_of_mags))

    # if filename given, write results as csv
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'wt') as f:
            writer = csv.writer(f, quoting = csv.QUOTE_ALL)
            writer.writerow(("name", "street", "city", "prov", "website"))
            for mag in list_of_mags:
                row = (mag.name, mag.street, mag.city, mag.prov, mag.website)
                writer.writerow(row)
    # otherwise print to screen
    else:
        for mag in list_of_mags:
            print(mag)
