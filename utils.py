#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.parse import urljoin, urlsplit, urlparse, urlunparse


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def relToAbsURL(base, url):
    """
    Return an absolute URL from the base URL and the current URL,
    we also clean everything after the # character
    """
    return urljoin(base, url).split("#")[0]


def domainName(url):
    """
    Return the domain name from the URL
    """
    return urlparse(url).netloc


def fileInfosFromURL(url):
    """
    Return the path and the filename of a file from an URL
    """
    return urlparse(url).path


def pathFromFileInfos(fileInfos):
    """
    Return the path of the file from an fileInfo 
    """
    return fileInfos.rsplit('/', 1)[0]


def filenameFromFileInfos(fileInfos):
    """
    Return the filename of the file from an fileInfo
    """
    return fileInfos.rsplit('/', 1)[1]


if __name__ == '__main__':
    print(fileInfosFromURL("http://www.creproulettes.fr/view/view.main.php"))
    print(fileInfosFromURL(pathFromFileInfos("http://www.creproulettes.fr/view/view.main.php")))
    print(fileInfosFromURL(filenameFromFileInfos("http://www.creproulettes.fr/view/view.main.php")))
