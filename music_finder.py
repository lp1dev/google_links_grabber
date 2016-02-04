#!/usr/bin/python3
# -*- coding: utf-8 -*-

from grabber import get_links, get_links_from_text
from concurrent.futures import ProcessPoolExecutor
from threading import active_count
from sys import argv
from time import sleep
import requests

max_threads=8
sleep_time = 0
query_string = 'index of last modified parent directory wma mp3 ogg %s'
indexof_identifiers=["Index of", "Name", "Last modified", "Size", "Description", "Parent Directory"]
verbose=True

def usage():
    print("usage : %s query" %argv[0])
    return 1

def is_indexof(text):
    for identifier in indexof_identifiers:
        if identifier not in text:
            if verbose:
                print("\t[Identifier %s not found]" %(identifier))
            return False
    return True

def fetch_file_links(link):
    r = requests.get("http://"+link)
    if verbose:
        print("fetching files on %s" %link)
    if not is_indexof(r.text):
        if verbose:
            print("\t[%s not an open dirlisting]" %link)
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

def get_matching_links(origin_url, links, query):
    matching_links = []
    query_terms = query.split(" ")
    for link in links:
        if type(link) == str and link[-4:].lower() == ".mp3":
            match = 0
            for term in query_terms:
                if verbose:
                    print("\t\t[Checking if %s in %s]" %(term.lower(), link.lower()))
                if term.replace(" ", "").lower() in link.lower():
                    if verbose:
                        print("\t\t[\033[0;32m%s FOUND in %s match +1\033[0;0m]" %(term, link)) 
                    match += 1
            if match == len(query_terms):
                matching_links.append(origin_url+link)
    return matching_links

def handle_link(link):
    file_links = fetch_file_links(link)
    matching_links = get_matching_links(link, file_links, argv[1])
    with open("output.txt", "a+") as f:
        for link in matching_links:
            f.write(link+"\n")

def main():
    if len(argv) != 2:
        return usage()
    links = get_links(query_string %argv[1], 0)
    for link in links:
        with ProcessPoolExecutor(max_workers=max_threads) as e:
            thread = [e.submit(handle_link, link)]
            sleep(sleep_time)
    return 0

if __name__ == "__main__":
    main()
