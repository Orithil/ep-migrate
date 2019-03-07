Eeagleplatform migrator
=======================

This python module helps you to get your videos from CDN platform by Rambler
and upload them on YouTube.
It uses eagleplatform-api calls documented
[here](https://github.com/dultonmedia/eagleplatform-api/) and Google
[YouTube API v3](https://developers.google.com/youtube/v3/).

Usage
-----

ptyhon3 -m eagleplatform_migrator -a ep_client_id.json -f filter_id

Both arguments required.

ep_client_id.json should have the folowing structure:
```json
{
    "address": "https://api.eagleplatform.com/media/",
    "account": "account_name",
    "auth_token": "secret_token"
}
```

```address``` here is static address defined in eagleplatform-api docs.
```account``` can be obtained from your eagleplatform server address. It looks like "**account_name**.new.eagleplatform.com"
```auth_token``` is generated in eagleplatform web interface. You should never make it public.

filter_id is the way to get specific subset of video files from your CDN account. You can only configure specific filter in eagleplatform web interface and get it's id from adressbar. It looks like "*account_name*.new.eagleplatform.com/filters/**filter_id**/"

Module will create new subdirectory media/ in working dir and put all the downloaded files there.
Filenames are generated from video title and video id.

For now to upload videos on YouTube you have to register this module as an app in [Google developers console](https://console.developers.google.com/) and issue a client_id.json.

TODO
----
- Add proper user authentication for YouTube.
- Review and possibly rewrite docs.
- Allow user to choose video privacy status on YouTube.
