#!/usr/bin/python3
# -*- coding: utf-8 -*-

from grabber import get_links, get_links_from_text
from concurrent.futures import ProcessPoolExecutor
from threading import active_count
from sys import argv
from time import sleep
import requests

max_threads=4
sleep_time = 0
query_string = 'intitle%%3A%%22index%%20of%%22%%20%%2B%%22last%%20modified%%22%%20%%2B%%22parent%%20directory%%22%%20%%2B(wma%%7Cmp3%%7Cogg)%%20%s'
indexof_identifiers=["Index of", "Name", "Last modified", "Size", "Description", "Parent Directory"]
verbose=True

def usage():
    print("usage : %s query" %argv[0])
    return 1

def fetch_file(link):
    r = requests.get("http://"+link)
    if verbose:
        print("fetching files on %s" %link)
    for identifier in indexof_identifiers:
        if identifier not in r.text:
            if verbose:
                print("[%s not in %s]" %(identifier, link))
            return False
    print("[%s passed test 1]" %link)
    print(get_links_from_text(r.text))

def main():
    if len(argv) != 2:
        return usage()
    links = get_links(query_string %argv[1], 0)
    for link in links:
        lol
        fetch_file(link)
        sleep(sleep_time)            
    return 0

if __name__ == "__main__":
    main()
