# -*- coding: utf-8 -*-

from __future__ import print_function
from __future__ import division

import urllib2
import requests



def get_one_piece_chapter_list():
    """Retrieves a list of chapters."""
    ms_page = "https://readms.net/manga/one_piece"

    jb_page = "https://jaiminisbox.com/reader/series/one-piece-2"
    # Pages don't have uniform structure, so thread carefully.
    
    # first, MS.
    ms_response = urllib2.urlopen(ms_page)
    ms_page = ms_reponse.read()
    print(ms_page)

if __name__ == "__main__":
    get_one_piece_chapter_list()


