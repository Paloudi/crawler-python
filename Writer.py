#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from utils import domainName, fileInfosFromURL, pathFromFileInfos, filenameFromFileInfos
from pathlib import Path

class Writer:
    URL = None
    HTML = None
    domain = None
    fileInfos = None
    filename = None
    path = None

    def __init__(self, URL, HTML):
        self.URL = URL
        self.HTML = HTML

        self.splitFromURL()
        self.createDomain()

    def splitFromURL(self):
        self.domain = domainName(self.URL)
        self.fileInfos = fileInfosFromURL(self.URL)
        self.path = pathFromFileInfos(self.fileInfos)
        try:
            self.filename = filenameFromFileInfos(self.fileInfos)
        except IndexError:
            self.filename = self.domain

    def createDomain(self):
        Path(self.domain).mkdir(parents=True, exist_ok=True)
        self.createFile()

    def createFile(self):
        Path(self.domain + self.path).mkdir(parents=True, exist_ok=True)
        try:
            with open(self.domain + self.path + '/' + self.filename + '.html', "w") as file:
                file.write(self.HTML)
        except OSError:
            print("File impossible to create")