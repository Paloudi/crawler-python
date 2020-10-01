#! /usr/bin/env python3
# -*- coding: utf-8 -*-

from urllib.request import urlopen
from urllib.error import HTTPError, URLError
import urllib.parse
from urllib.parse import urlparse


from multiprocessing import Process, Pool, Queue, cpu_count, Value, log_to_stderr
import os, signal, logging

from utils import relToAbsURL, bcolors, domainName
from Parser import Parser
from Writer import Writer
from time import sleep

mp1 = log_to_stderr(logging.INFO)

class CrawlerMaster:
    """
    Manage the crawlers
    """
    URL = None
    depth = None
    domainBool = None
    domainName = None
    numPages = None
    crawlerQueue = None

    def __init__(self, URL, depth, domainBool):
        print("CrawlerMaster n°" + str(os.getpid()) + " starting his job")
        self.URL = URL
        self.depth = depth
        self.domainBool = domainBool
        self.setupQueue()
        self.setSameDomain()
        self.numPages = Value('i', 0)
        while self.crawlerQueue.qsize() != 0:
            processes = []
            while len(processes) <= cpu_count() and self.crawlerQueue.qsize() > 0:
                processes.append(Process(target=Crawler, args=(self.crawlerQueue, self.domainName, self.numPages)))
            for p in processes:
                p.start()
            for p in processes:
                p.join()
                # p.terminate()
        print(f"{bcolors.OKGREEN}Queue emptied{bcolors.ENDC}")

    def setupQueue(self):
        self.crawlerQueue = Queue()
        self.crawlerQueue.put((self.URL, self.depth))

    def setSameDomain(self):
        if self.domainBool:
            self.domainName = urlparse(self.URL).netloc
        else:
            self.domainName = None


class Crawler:
    """
    Crawl a website and parse it
    """
    pid = None
    crawlerQueue = None
    domain = None
    URL = None
    depth = None
    parser = None
    html = None
    numPages = None
    alreadyParsed = set()

    def __init__(self, crawlerQueue, domain, numPages):
        self.pid = os.getpid()
        print("Crawler n°" + str(self.pid) + " starting his job...")
        self.crawlerQueue = crawlerQueue
        self.unpackTuple()
        if domain is not None:
            self.domain = domain
        self.numPages = numPages
        self.printInfos()
        print("page number n°" + str(self.numPages.value))
        self.numPages.value += 1
        try:
            self.initializeParser()
            self.writeToFile()
        except HTTPError as e:
            print(f"{bcolors.FAIL}ERROR: " + str(e) + f"{bcolors.ENDC}")
        except URLError as e:
            print(f"{bcolors.FAIL}ERROR: " + str(e) + f"{bcolors.ENDC}")

        print("Crawler n°" + str(self.pid) + " stopping his job...")

    def unpackTuple(self):
        tupleURLDepth = self.crawlerQueue.get(False)
        self.URL = tupleURLDepth[0]
        self.depth = tupleURLDepth[1]

    def writeToFile(self):
        pass
        # writer = Writer(self.URL, self.html)

    def printInfos(self):
        print(f"{bcolors.HEADER}Crawler working on " + self.URL + f"{bcolors.ENDC}")
        print(f"Crawler depth is set to {bcolors.WARNING}" + str(self.depth) + f"{bcolors.ENDC}")

    def initializeParser(self):
        self.openURL()
        self.parser = Parser()
        self.parser.feed(self.html)
        self.callNewCrawler()

    def callNewCrawler(self):
        if self.depth > 0:
            newDepth = self.depth - 1
        elif self.depth == 0 and self.crawlerQueue.qsize() >= 0:
            newDepth = self.depth
        else:
            print(f"{bcolors.FAIL}Crawler n°" + str(self.pid) + " lost, we shouldn't be here!"+f"{bcolors.ENDC}")
            exit(-1)
        if not self.URL in Crawler.alreadyParsed:
            Crawler.alreadyParsed.add(self.URL)
            for link in set(self.parser.getUrls()):
                absLink = relToAbsURL(self.URL, link)
                if self.domain is not None and self.domain == urlparse(absLink).netloc:
                    if absLink in Crawler.alreadyParsed:
                        print(f"{bcolors.WARNING}Crawler n°" + str(self.pid) + " skipping " + absLink + f"{bcolors.ENDC} (already parsed)")
                    else:
                        print(f"{bcolors.OKGREEN}Crawler n°" + str(self.pid) + " adding " + str(absLink) + f"{bcolors.ENDC}")
                        newTuple = (absLink, newDepth)
                        self.crawlerQueue.put(newTuple, False)
                        print("Queue size : " + str(self.crawlerQueue.qsize()))
                else:
                    print(f"{bcolors.WARNING}Crawler n°" + str(self.pid) + " skipping " + absLink + f"{bcolors.ENDC} (same-domain policy)")
                # sleep(0.1)

    def openURL(self):
        """
        Open an URL
        """
        try:
            request = urlopen(self.URL, timeout=2)
        except UnicodeEncodeError:
            iri = self.URL
            iriSplit = iri.split('//')
            url = iriSplit[0] + '//' + urllib.parse.quote(iriSplit[1])
            request = urlopen(url)
        try:
            self.html = request.read().decode(request.headers.get_content_charset())
        except TypeError:
            self.html = request.read().decode('utf-8')
