import urllib.request
import urllib.error
import json
import sys
import requests
from pathlib import Path
from eagleplatform_migrator.helpers import savelist, cprint, home_size, reporthook


def get_records(site, login, token, request_type, filter_id):
    """ Make api request to cdn server.

    Keyword arguments:
    site -- server url
    login, token -- server access credentials. Obtained in server's web interface
    request_type -- defines if request supposed to get records list by filter or individual record.
    filter_id -- used to define individual record id or filter id to get records list.
    """
    cprint('info', "Making api request")
    while True:
        try:
            response = requests.get(
                f"{site}{request_type}/{filter_id}.json?per_page=all&account={login}&auth_token={token}")
            if response.status_code == 200:
                try:
                    records = json.loads(response.text)
                    if records['status'] == 200:
                        return records['data']
                    else:
                        cprint(
                            'error', F"Failed to get records due to an error: \n\t{records['errors'][0]}")
                        sys.exit(2)
                except json.decoder.JSONDecodeError:
                    cprint('error', 'Response is not JSON. Is address correct?')
            else:
                cprint('error', "404. Failed to get records. Is address correct?")
                sys.exit(2)
        except (ConnectionResetError, requests.exceptions.ConnectionError) as e:
            cprint(
                'error', f"Error occured on api request to filters: \n\t{e}\nRetrying...")


def get_file(videolink, filename):
    """ Download file from given link to destination with filename. """
    while True:
        cprint('info', f"Trying to download {filename}")
        videofile = Path(filename)
        if videofile.is_file():
            cprint(
                'info', f"File {filename} already exists.\n\tSkip downloading.")
            break

        else:
            try:
                urllib.request.urlretrieve(
                    videolink, filename, reporthook)
                cprint('success', "\nSuccess!")
                break

            except (ConnectionResetError, requests.exceptions.ConnectionError, urllib.error.URLError) as e:
                cprint(
                    'error', f"Error occured on getting file {filename}: \n\t{e}")


def get_videos(site, login, token, filter_id):
    """ Downloads records from records list and saves list of downloaded files with id, name and filepath in JSON format. 

    Keyword arguments:
    site -- server url
    login, token -- server access credentials. Obtained in server's web interface
    filter_id -- used to define individual record id or filter id to get records list.
    """
    records_list = get_records(site, login, token, 'filters', filter_id)

    videolist = {'records': []}

    for entry in reversed(records_list['records']):
        cprint('info', f"Making api request to get {entry['name']}")
        video = get_records(site, login, token, 'records', entry['id'])
        videolink = video['record']['origin']
        filename = f"media/{entry['name']}_{entry['id']}.mp4"

        get_file(videolink, filename)

        videolist['records'].append(
            {'eagle_id': entry['id'], 'name': entry['name'], 'filename': filename})

        if home_size() < 2:
            savelist(
                f"videolist_{videolist['records'].index(entry)}.json", videolist)
            cprint(
                'warning', f"Critical space left in 'home'\nStopped processing at {videolist['records'].index(entry)}-th entry\n")
            break

    savelist("videolist_full.json", videolist)
    return videolist
