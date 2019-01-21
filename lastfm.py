import os

from lastfmclient import LastfmClient


def milli_seconds_to_duration(milli_seconds):
    total_seconds = milli_seconds / 1000

    minutes = total_seconds / 60
    seconds = total_seconds % 60

    return 'PT{}M{}S'.format(minutes, seconds)


def get_lastfm_most_recently_listened_details():
    lastfm_key = os.environ.get('lastfm_key')
    lastfm_secret = os.environ.get('lastfm_secret')

    lastfm_client = LastfmClient(lastfm_key, lastfm_secret)
    recent_tracks = lastfm_client.user.get_recent_tracks('kevbear')['track']
    recent_track = recent_tracks[0]
    artist_name = recent_track['artist']['#text']
    track_name = recent_track['name']
    mbid = recent_track['mbid']
    track_info = lastfm_client.track.get_info(
        artist_name,
        track_name,
        mbid,
    )
    lastfm_result = {
        'track': track_info['name'],
        'duration': milli_seconds_to_duration(int(track_info['duration'])),
        'album': track_info['album']['title'],
        'artist': track_info['artist']['name'],
        'url': track_info['url'],
    }

    return lastfm_result
