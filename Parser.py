#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from html.parser import HTMLParser


class Parser(HTMLParser):
    urls = []

    def __init__(self):
        super().__init__()


    def handle_starttag(self, tag, attr):
        """
        Handle the start tags of the HTML
        """
        if tag == "a":
            try:
                self.urls.append(dict(attr)['href'])
            except KeyError:
                pass

    def getUrls(self):
        return self.urls
