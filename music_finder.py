#!/usr/bin/python3
# -*- coding: utf-8 -*-

from grabber import get_links, get_links_from_text
from concurrent.futures import ProcessPoolExecutor
from threading import active_count
from sys import argv
from time import sleep
from flask import jsonify
import json
import requests
import redis

max_threads=10
sleep_time = 0
query_string = 'index of last modified parent directory wma mp3 ogg %s'
indexof_identifiers=["Index of", "Name", "Last modified", "Size", "Description", "Parent Directory"]
verbose=True
threaded=False

def db_connect():
    return redis.StrictRedis(host="2.lp1.eu", port=6379, db=0)

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
                try:
                    if verbose:
                        print("\t\t[Checking if %s in %s]" %(term.lower(), link.lower()))
                    if term.replace(" ", "").lower() in link.lower():
                        if verbose:
                            print("\t\t[\033[0;32m%s FOUND in %s match +1\033[0;0m]" %(term, link)) 
                        match += 1
            if match == len(query_terms):
                matching_links.append(origin_url+link)
    return matching_links

def handle_link(query, link):
    file_links = fetch_file_links(link)
    matching_links = get_matching_links(link, file_links, argv[1])
    for link in matching_links:
        save_in_db(query, link)

        
def save_in_db(query, link):
    links_array = r.get(query)
    if links_array is None:
        links_array = "[]"
    else:
        links_array = links_array.decode("utf-8")
    links_array = json.loads(links_array)
    links_array.append(link)
    r = db_connect()
    r.set(query, jsonify(links_array))
    print("Getting value in redis for %s : [%s]" %(query, r.get(query)))

def check_in_db(query):
    query_terms = query.split(" ")
    r = db_connect()
    results = {}
    found_terms = 0
    for term in query_terms:
        for key in r.keys("*"):
            if term in key.decode("utf-8"):
                found_terms += 1
    if found_terms >= len(query_terms) - 1:
        link_list = json.loads(r.get(key).decode("utf-8"))
        results[key.decode("utf-8")] = link_list
        return results, True
    return results, False
    
def main():
    if len(argv) != 2:
        return usage()
    results, exists = check_in_db(argv[1])
    if exists:
        print(results)
        return
    links = get_links(query_string %argv[1], 0)
    for link in links:
        if threaded:
            with ProcessPoolExecutor(max_workers=max_threads) as e:
                thread = [e.submit(handle_link, argv[1], link)]
                sleep(sleep_time)
        else:
            handle_link(argv[1], link)
    return 0

if __name__ == "__main__":
    main()
