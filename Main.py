#! /usr/bin/env python3
# -*- coding: utf-8 -*-

import argparse
from Crawler import Crawler, CrawlerMaster

if __name__ == '__main__':
    parser = argparse.ArgumentParser(prog='Crawler', description='Crawl a website and download it')
    parser.add_argument('--url', '-u', metavar='URL', type=str, required=True,
                        help='The URL to crawl')
    parser.add_argument('--depth', '-d', metavar='N', dest='depth', type=int, default=3,
                        help='Indicate the depth of the crawling (default: 3)')
    parser.add_argument('--same-domain','-s', default=False, dest='domain', action='store_true',
                        help='Restrain the crawler to the current domain')
    args = parser.parse_args()
    crawlerMaster = CrawlerMaster(args.url, args.depth, args.domain)
    # crawler = Crawler(args.url, args.depth, args.domain)
