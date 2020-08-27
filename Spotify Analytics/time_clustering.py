# Import required packages
import random
import re
import time
import pandas as pd
import spotipy, spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
from itertools import islice, chain, repeat

# Load Spotify API credentials
file = open("spotipy_credentials.txt", "r")
text = [re.sub("\n","",txt) for txt in file.readlines()]
values = {}

for i, item in enumerate(text):
    temp = item.split(" = ")
    values.update({temp[0]: temp[1]})

### Authenticating Spotify API & Starting Session
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

# Clustering by time
df = pd.read_excel("eng_features.xlsx")
df.sort_values(by=['year','artist','track_name'], ascending=True, inplace=True)
df.reset_index(drop=True, inplace=True)

sub_playlists = {}

oldies = df[df['year']<=2003].copy()
oldies.reset_index(drop=True, inplace=True)
sub_playlists.update({"KJ's Oldies":oldies})

song_2000s = df[(df['year']>=2004)&(df['year']<=2011)].copy()
song_2000s.reset_index(drop=True, inplace=True)
sub_playlists.update({"KJ's 2000s":song_2000s})

song_2010s = df[(df['year']>=2012)&(df['year']<=2014)].copy()
song_2010s.reset_index(drop=True, inplace=True)
sub_playlists.update({"KJ's 2010s":song_2010s})

new_pop =  df[df['year']>=2015].copy()
new_pop.reset_index(drop=True, inplace=True)
sub_playlists.update({"KJ's Post 2015s":new_pop})

# Function to chunk songs (max 50 can be added each time)
_no_padding = object()

def chunk(it, size, padval=_no_padding):
    if padval == _no_padding:
        it = iter(it)
        sentinel = ()
    else:
        it = chain(iter(it), repeat(padval))
        sentinel = (padval,) * size
    return iter(lambda: tuple(islice(it, size)), sentinel)

# Create playlists
for name in list(sub_playlists.keys()):
    sp.user_playlist_create(user=username,
                            name=name)

# Add songs into each playlist
for i, playlist in enumerate(list(sub_playlists.values())):
    keys = list(sub_playlists.keys())
    user_playlists = sp.current_user_playlists()

    for pl in user_playlists['items']:
        if pl['name'] == keys[i]:
            playlist_uri = pl['uri'].split(":")[-1]
            break

    for item in list(chunk(range(len(playlist)), 50)):
        sp.user_playlist_add_tracks(username,
                                    playlist_uri,
                                    playlist['uri'][item[0]:item[-1]+1].to_list())
        time.sleep(random.randint(5,8))
