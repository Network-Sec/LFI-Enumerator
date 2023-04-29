#!/usr/bin/env python3

import requests
import os
import argparse

DEBUG = True

def check_path(url, path):
    proxies = {}
    if DEBUG:
        proxies = {"http": "http://localhost:8080", "https": "http://localhost:8080"}

    response = requests.get(url + path, proxies=proxies)

    if DEBUG and response.status_code == 200:
        print(response.request.url, response.status_code)
    
    return response.status_code, response

def is_file(url, path, response):
    if len(response.text) > 50:
        return True
    status_code, _ = check_path(url, os.path.join(path, "."))
    return status_code != 200

def enumerate_files_dirs(url, path, wordlist, real_structure_set):
    custom_files = []
    structure = []

    for item in wordlist:
        if path:
            full_path = os.path.join(path, item)
        else:
            full_path = item
        status_code, response = check_path(url, full_path)

        if status_code == 200:
            structure.append(full_path)

            if full_path not in real_structure_set:  # Check if the file is standard or custom
                if DEBUG:
                    print(full_path)
                custom_files.append(full_path)

            if not is_file(url, full_path, response):  # If it's a directory, perform recursive search
                if DEBUG:
                    print("Recursing:", full_path)
                custom_files.extend(enumerate_files_dirs(url, full_path, wordlist, real_structure_set))

    return custom_files, structure

# Argument handling
parser = argparse.ArgumentParser(description="Webserver enumeration and deviation finder")
parser.add_argument("url", help="URL to send GET requests")
parser.add_argument("basename", help="Basename for the output files")
parser.add_argument("wordlist", help="Wordlist file containing default Linux files and directories")
parser.add_argument("real_structure_wordlist", help="Wordlist file containing the real structure of a Linux system")
args = parser.parse_args()

url = args.url
basename = args.basename
wordlist_file = args.wordlist
real_structure_wordlist_file = args.real_structure_wordlist

# Read wordlist file
with open(wordlist_file, "r") as f:
    wordlist = [line.strip() for line in f]

# Read real_structure_wordlist file and build a set
with open(real_structure_wordlist_file, "r") as f:
    real_structure_set = set(line.strip() for line in f)

# Start recursive enumeration
deviations, structure = enumerate_files_dirs(url, "", wordlist, real_structure_set)

# Save structure
with open(f"{basename}_structure.txt", "w") as f:
    for item in structure:
        f.write(f"{item}\n")

# Save deviations
with open(f"{basename}_deviations.txt", "w") as f:
    for deviation in deviations:
        f.write(f"{deviation}\n")
