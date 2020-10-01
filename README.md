# crawler-python
basic crawler in OOP Python
Crawl websites using multiprocessing then reconstruct the website skeleton with folders and html files.

usage: Crawler [-h] --url URL [--depth N] [--same-domain]

Crawl a website and download it

optional arguments:
  -h, --help         show this help message and exit
  --url URL, -u URL  The URL to crawl
  --depth N, -d N    Indicate the depth of the crawling (default: 3)
  --same-domain, -s  Restrain the crawler to the current domain
