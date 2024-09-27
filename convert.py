from tqdm import tqdm
import pandas as pd
from time import sleep
from ytmusicapi import YTMusic


def search_for_artist(ytmusic, artist):
    search_query = f"{artist['name']}" if type(artist) == dict else artist
    results = ytmusic.search(
        search_query, filter="artists", ignore_spelling=True)
    browseId = results[0]['browseId']
    channel_id = ytmusic.get_artist(browseId)['channelId']
    return channel_id


def search_for_artist_with_track_name(ytmusic: YTMusic, search_str: str):
    try:
        return ytmusic.search(search_str, filter="songs", ignore_spelling=True)[0]["artists"][0]["id"]
    except:
        return None


def search_for_album(ytmusic, album):
    search_query = f"{album['album']}"
    if album['artist'] != "Various Artists":
        search_query += f" {album['artist']}"

    results = ytmusic.search(
        search_query, filter="albums", ignore_spelling=True)
    return results[0]['playlistId']


def search_for_track(ytmusic, track):
    search_query = f"{track['track']} {track['artist']}" if type(
        track) == dict else track
    results = ytmusic.search(
        search_query, filter="songs", ignore_spelling=True)
    return results[0]['videoId']


def uri_to_url(uri):
    _, type_, id_ = uri.split(':')
    return f'https://open.spotify.com/{type_}/{id_}'


def get_channel_id(channel_uri):
    return channel_uri.split("channel/")[-1]


def channel_url(channel_id):
    return f"https://music.youtube.com/channel/{channel_id}"


def get_vid_ids(ytmusic, playlist):
    vid_ids = []
    for item in tqdm(
            playlist,
            desc='Spotify->YouTube',
            unit='track'
    ):
        yt_track = search_for_track(ytmusic, item['track']['trackUri'])
        vid_ids.append(yt_track)

    return vid_ids


def convert_to_playlist(ytmusic, src_playlist, desc="", privacy="PRIVATE"):
    vids = get_vid_ids(ytmusic, src_playlist)
    ytplaylist = ytmusic.create_playlist(
        src_playlist['name'],
        description=src_playlist['description'] or desc,
        privacy_status=privacy
    )
    return ytmusic.add_playlist_items(ytplaylist, vids)


def get_all_artist_cids(ytmusic: YTMusic,
                        library_artists: dict,
                        full_streaming_history: pd.DataFrame = None,
                        sleeptime: int = 5
                        ):

    artists = pd.DataFrame(library_artists)
    artists['channelId'] = ""
    artists['test_track'] = ""

    batch = 100
    search_errors = []
    for i, row in tqdm(artists.iterrows(), total=len(artists)):
        if row["channelId"] == "":
            try:
                artists.loc[i, 'channelId'] = search_for_artist(
                    ytmusic, row["name"])
            except:
                print(f"Error with {row['name']}")
                search_errors.append(i)

            if i % batch == 0:
                tqdm.write(f"Sleeping for {sleeptime} seconds")
                sleep(sleeptime)

    if full_streaming_history is not None:
        for index, row in artists.iterrows():
            test_track = ""
            if row["name"] in full_streaming_history["master_metadata_album_artist_name"].values:
                test_track = full_streaming_history[full_streaming_history["master_metadata_album_artist_name"]
                                                    == row["name"]].iloc[0]['master_metadata_track_name']
            artists.loc[index, 'test_track'] = test_track

        track_search_errors = []
        fixed = []

        for index, row in tqdm(artists.iterrows(), total=len(artists)):
            if row["test_track"] != "":
                correct_id = search_for_artist_with_track_name(
                    ytmusic, f"{row['test_track']} {row['name']}")

                if correct_id is not None and correct_id != row["channelId"]:
                    fixed.append([
                        index,
                        row["name"],
                        row["channelId"],
                        correct_id
                    ])
                    artists.loc[index, 'channelId'] = correct_id

                elif correct_id is None:
                    track_search_errors.append(index, ytmusic.search(
                        f"{row['name']} - {row['test_track']}", filter="songs", ignore_spelling=True))

        if track_search_errors:
            log = [print(f"{artists.iloc[k[0]]['name']} - {artists.iloc[k[0]]['test_track']}",
                   channel_url(artists.iloc[k[0]]["channelId"])) for k in track_search_errors]

        artists.to_csv("artists_with_track_search.csv", index=False)
        return artists, fixed, track_search_errors, search_errors

    else:
        artists.to_csv("artists_without_track_search.csv", index=False)
        return artists, search_errors
