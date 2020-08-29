# Import required packages
import re
import pandas as pd
import spotipy, spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials

# Load Spotify API credentials
file = open("spotipy_credentials.txt", "r")
text = [re.sub("\n","",txt) for txt in file.readlines()]
values = {}

for i, item in enumerate(text):
    temp = item.split(" = ")
    values.update({temp[0]: temp[1]})

### Getting list of all audio features from already created Spotify playlist
username = values['username']
scope = values['scope']
cid = values['cid']
secret = values['secret']

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
sp.trace=False

token = util.prompt_for_user_token(username,
                                   scope,
                                   client_id=cid,
                                   client_secret=secret,
                                   redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token)

playlists = [{"playlist_id": '5ylrlfh6RzjgqA1lGjs7Cs', "output_name": "eng_features.xlsx"},
             {"playlist_id": '3k5BdcCPKDsLx8gnUlRLIY', "output_name": "kor_features.xlsx"},
             {"playlist_id": '2l0yjtIHDxmTioYS1GvpaS', "output_name": "chi_features.xlsx"}]

for pl_i, item in enumerate(playlists):
    df_main = pd.DataFrame()
    offset_amt = 0

    while True:
        playlist = sp.playlist_tracks(item["playlist_id"], offset=offset_amt)
        songs = playlist['items']

        ids = []
        add_features = []

        for i, song in enumerate(songs):
            if song['track']['id']:
                ids.append(song['track']['id'])
            else:
                continue # Skip song if there is no id (aka local, not Spotify song)

            add_info = {}

            # Extracting artists
            if len(song['track']['artists']) > 1:
                artists = []

                for artist in song['track']['artists']:
                    artists.append(artist['name'])

                artists = ", ".join(artists)
                add_info.update({"artist": artists})
            else:
                add_info.update({"artist": song['track']['artists'][0]['name']})

            # Extract track name
            add_info.update({"track_name": song['track']['name']})

            # Extract year
            add_info.update({"year": int(song['track']['album']['release_date'][:4])})

            # Extract popularity
            add_info.update({"popularity": int(song['track']['popularity'])})

            add_features.append(add_info)

        features = sp.audio_features(ids)
        df_features = pd.DataFrame(features)

        df_add_features = pd.DataFrame(add_features)
        df_features = pd.concat([df_add_features, df_features], axis=1)

        df_main = pd.concat([df_main, df_features], axis=0)

        if playlist['next']:
            offset_amt += 100
        else:
            break

    df_main.sort_values(by=["artist","track_name"], inplace=True)
    df_main.reset_index(drop=True, inplace=True)
    df_main.to_excel(item["output_name"], index=False, engine='xlsxwriter')
