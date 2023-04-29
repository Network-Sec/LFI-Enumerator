#!/usr/bin/env python3

import requests
import os
import argparse

def check_path(url, path):
    response = requests.get(url + path)
    return response.status_code, response

def is_file(url, path, response):
    if len(response.text) > 50:
        return True
    status_code, _ = check_path(url, os.path.join(path, "."))
    return status_code != 200

def enumerate_files_dirs(url, path, wordlist):
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

            if is_file(url, full_path, response):  # Checking if it's a file
                with open(f"{basename}_readable_files.txt", "a") as readable_file:
                    readable_file.write(f"{full_path}\n{response.text}\n\n")
                custom_files.append(full_path)
            else:  # If it's a directory, perform recursive search
                custom_files.extend(enumerate_files_dirs(url, full_path, wordlist))

    return custom_files, structure

# Argument handling
parser = argparse.ArgumentParser(description="Webserver enumeration and deviation finder")
parser.add_argument("url", help="URL to send GET requests")
parser.add_argument("basename", help="Basename for the output files")
parser.add_argument("wordlist", help="Wordlist file containing default Linux files and directories")
args = parser.parse_args()

url = args.url
basename = args.basename
wordlist_file = args.wordlist

# Read wordlist file
with open(wordlist_file, "r") as f:
    wordlist = [line.strip() for line in f]

# Start recursive enumeration
deviations, structure = enumerate_files_dirs(url, "", wordlist)

# Save structure
with open(f"{basename}_structure.txt", "w") as f:
    for item in structure:
        f.write(f"{item}\n")

# Save deviations
with open(f"{basename}_deviations.txt", "w") as f:
    for deviation in deviations:
        f.write(f"{deviation}\n")
