#! /usr/bin/env python3

import argparse
import requests
import json
import urllib.request
import urllib.error
import time
import shutil
import sys
from colorama import init
from colorama import Fore
from pathlib import Path


def main():

    init(autoreset=True)

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth", help="JSON file with server address, account name and auth token")
    parser.add_argument(
        "-f", "--filter", help="Filter ID. Filter and its ID can be set in site's web interface")
    args = vars(parser.parse_args())

    try:
        with open(args['auth'], "r") as cred:
            credentials = json.load(cred)
    except AttributeError:
        print(
            "You have to provide valid sredentials file in form { 'address': 'example.com', 'account': 'myaccount', 'auth_token': 'secret' }")
        sys.exit(1)

    site = credentials['address']
    login = credentials['account']
    token = credentials['auth_token']
    filter_id = args['filter']

    while True:
        cprint('info', "Making api request")
        try:
            records_list = requests.get(
                f"{site}filters/{filter_id}.json?per_page=all&account={login}&auth_token={token}")
            break
        except (ConnectionResetError, requests.exceptions.ConnectionError) as e:
            cprint(
                'error', f"Error occured on api request to filters: \n\t{e}")

    if records_list.status_code != "200":
        records = json.loads(records_list.text)
        videolist = {'records': []}
        for record in records['data']['records']:
            videolist['records'].append(
                {'eagle_id': record['id'], 'name': record['name']})

    count = 0
    for entry in reversed(videolist['records']):
        while True:
            cprint('info', f"Making api request to get {entry['name']}")
            try:
                videolink = json.loads(requests.get(
                    f"{site}records/{entry['eagle_id']}.json?account={login}&auth_token={token}").text)
                cprint('info', f"Trying to download {entry['name']}")

                videofile = Path(f"media/{entry['name']}.mp4")

                if videofile.is_file():
                    cprint(
                        'info', f"File 'media/{entry['name']}.mp4' already exists.\n\tSkip downloading.")
                    count += 1
                    break

                else:
                    try:
                        urllib.request.urlretrieve(
                            videolink['data']['record']['origin'], f"media/{entry['name']}.mp4", reporthook)
                        cprint('success', "\nSuccess!")
                        count += 1
                        break

                    except (ConnectionResetError, requests.exceptions.ConnectionError, urllib.error.URLError) as e:
                        cprint(
                            'error', f"Error occured on getting file {entry['name']}: \n\t{e}")

            except (ConnectionResetError, requests.exceptions.ConnectionError) as e:
                cprint(
                    'error', f"Error occured on api request to record {entry['name']}: \n\t{e}")

        videolist['records'][videolist['records'].index(
            entry)]['filename'] = f"media/{entry['name']}.mp4"
        if not count % 100:
            cprint('info', "100 entries poceeded.\nMaking intermediary dump.")
            savelist(f"videolist_{count}.json", videolist)

        if home_size() < 2:
            savelist(
                f"videolist_{videolist['records'].index(entry)}.json", videolist)
            cprint(
                'warning', f"Critical space left in 'home'\nStopped processing at {videolist['records'].index(entry)}-th entry\n")
            break

    savelist("videolist_full.json", videolist)


def savelist(filename, jsondict):
    with open(filename, "w") as file:
        json.dump(jsondict, file, indent=2, ensure_ascii=False)
        cprint('success', f"JSON dumped to {filename}\nDone!")


def cprint(type, message):
    types = {'error': Fore.RED, 'info': Fore.CYAN,
             'warning': Fore.MAGENTA, 'success': Fore.GREEN}
    type = types[type]
    print(f"{type}{message}")


def home_size():
    return int(shutil.disk_usage("/home")[2] / (1024**3))


def reporthook(count, block_size, total_size):
    global start_time
    if count == 0:
        start_time = time.time()
        return
    duration = time.time() - start_time
    progress_size = int(count * block_size)
    speed = int(progress_size / (1024 * duration))
    percent = int(count * block_size * 100 / total_size)
    sys.stdout.write("\r...%d%%, %d MB, %d KB/s, %d seconds passed" %
                     (percent, progress_size / (1024 * 1024), speed, duration))
    sys.stdout.flush()


if __name__ == '__main__':
    main()
