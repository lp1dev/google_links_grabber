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

def is_indexof(text):
    for identifier in indexof_identifiers:
        if identifier not in text:
            print("[Identifier %s not found]" %(identifier))
            return False
    return True

def fetch_file_links(link):
    r = requests.get("http://"+link)
    if verbose:
        print("fetching files on %s" %link)
    if not is_indexof(r.text):
        if verbose:
            print("[%s not an open dirlisting]" %link)
        return []
    links = []
    splits = r.text.split('a href="')
    for split in splits:
        find = split.find('"')
        if split.find('<') < find:
            find = split.find('<')
        if len(split[:find]) > 0:
            links.append(split[:find].replace("&amp;prev=search", ""))
    return links

def get_matching_links(links, query):
    matching_links = []
    query_terms = query.split(" ")
    for link in links:
        if link[-4:] == ".mp3":
            match = 0
            for term in query_terms:
                if term in link:
                    match += 1
            if match >= 1:
                links.append(matching_links)
    return matching_links

def main():
    if len(argv) != 2:
        return usage()
    links = get_links(query_string %argv[1], 0)
    for link in links:
        file_links = fetch_file_links(link)
        matching_links = get_matching_links(file_links, argv[1])
        print(matching_links)
        sleep(sleep_time)
    return 0

if __name__ == "__main__":
    main()
