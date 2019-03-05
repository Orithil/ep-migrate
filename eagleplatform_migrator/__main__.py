#!/usr/bin/env python3

import argparse
import json
import sys
from eagleplatform_migrator.helpers import cprint
from eagleplatform_migrator.cdn_downloader import get_videos
from eagleplatform_migrator.youtube_uploader import youtube_upload


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--auth", required=True, help="JSON file with server address, account name and auth token")
    parser.add_argument(
        "-f", "--filter", required=True, help="Filter ID. Filter and its ID can be set in site's web interface")
    args = vars(parser.parse_args())

    try:
        with open(args['auth'], "r") as cred:
            credentials = json.load(cred)
    except AttributeError:
        cprint('error',
               "You have to provide valid sredentials file in form { 'address': 'example.com', 'account': 'myaccount', 'auth_token': 'secret' }")
        sys.exit(1)

    site = credentials['address']
    login = credentials['account']
    token = credentials['auth_token']
    filter_id = args['filter']

    records_list = get_videos(site, login, token, filter_id)

    youtube = youtube_upload(records_list['records'])
    youtube_response = json.loads(youtube)
    cprint('warning', youtube_response['id'])


if __name__ == '__main__':
    main()
