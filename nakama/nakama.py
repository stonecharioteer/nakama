# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import urllib2
import requests


import urllib2
import bs4
import datetime


def grouper(iterable, n, fillvalue=None):
    """Collect data into fixed-length chunks or blocks
    Example:
        >>> grouper('ABCDEFG', 3, 'x') --> ABC DEF Gxx
    """
    import sys
    if "2.7" in sys.version:
        from itertools import izip_longest as zip_longest
    else:
        from itertools import ziplongest
    args = [iter(iterable)] * n
    return list(zip_longest(*args, fillvalue=fillvalue))

def get_headers():
    """Returns the user agent and header so that urllib can work without a glitch.
    
    Mimics Firefox/Chrome.
    """
    
    hdr = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.11 (KHTML, like Gecko) Chrome/23.0.1271.64 Safari/537.11',
       'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
       'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
       'Accept-Encoding': 'none',
       'Accept-Language': 'en-US,en;q=0.8',
       'Connection': 'keep-alive'}
    
    return hdr

def rem_accents(s):
    import unicodedata
    search_string = ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    return search_string

def get_latest_one_piece_chapter_jb():
    """Retrieves the latest chapter number on Jaimini's box."""
    today = datetime.date.today()
    jb_page = "https://jaiminisbox.com/reader/series/one-piece-2"
    jb_request = urllib2.Request(jb_page, headers=get_headers())
    jb_response = urllib2.urlopen(jb_request)
    jb_page = jb_response.read()
    jb_page_soup = bs4.BeautifulSoup(jb_page, "html.parser")
    rows = jb_page_soup.find_all("div", attrs={"class":"element"})
    text = [row.text.strip() for row in rows]
    chapter_data = []
    for chapter in text:
        chapter_number = int(chapter.split()[1][:-1])
        chapter_name = rem_accents(chapter.split(":")[1].split("\n")[0].strip())
        release_date = chapter.split("by Jaimini's~Box~, ")[1].strip()
        if release_date.lower() == "today":
            release_date = datetime.date.today()
        elif release_date.lower() == "yesterday":
            release_date = datetime.date.today() - datetime.timedelta(days=1)
        else:
            release_date = datetime.datetime.strptime(release_date, "%Y.%m.%d").date()

        data = {
            "chapter_number": chapter_number,
            "chapter_name": chapter_name,
            "release_date": release_date,
            "days_passed": (datetime.date.today() - release_date).days
        }
        chapter_data.append(data)

    most_recent = [chapter for chapter in chapter_data if chapter["days_passed"] == min([chapter_row["days_passed"] for chapter_row in chapter_data])]
    return most_recent[0]

    
def get_latest_one_piece_chapter_ms():
    """Retrieves the latest chapter number and title on MS."""
    ms_page = "https://readms.net/manga/one_piece"
    # Pages don't have uniform structure, so thread carefully.
    # first, MS.
    ms_request = urllib2.Request(ms_page, headers=get_headers())
    ms_response = urllib2.urlopen(ms_request)
    ms_page = ms_response.read()
    ms_page_soup = bs4.BeautifulSoup(ms_page, "html.parser")
    
    table_rows = ms_page_soup.find_all("table")[0].find_all("td")
    
    data = [x.text for x in table_rows]
    paired_data = grouper(data, 2)
    
    chapter_data = []
    for pair in paired_data:
        date_string = pair[1]
        if date_string.lower() == "today":
            stripped_date = datetime.date.today()
        elif date_string.lower() == "1 day ago":
            stripped_date = datetime.date.today() - datetime.timedelta(days=1)
        else:
            try:
                stripped_date = pair[1].replace("th","").replace("nd","").replace("st","").replace("rd","")
                stripped_date = datetime.datetime.strptime(stripped_date, "%b %d, %Y").date()
            except ValueError:
                raise
        
        data = {
            "chapter_number": int(pair[0].split("-")[0].strip()),
            "chapter_name": pair[0].split("-")[1].strip(),
            "release_date": stripped_date,
            "days_passed": (datetime.date.today() - stripped_date).days
        }
        chapter_data.append(data)

    most_recent = [chapter for chapter in chapter_data if chapter["days_passed"] == min([chapter_row["days_passed"] for chapter_row in chapter_data]) ]
    return most_recent[0]

if __name__ == "__main__":
    pass


