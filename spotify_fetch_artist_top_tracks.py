import streamlit as st
import pandas as pd
import numpy as np

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

from st_utils import StProgress

st.title('Spotify artist info downloader')

DATA_URL = ('./artist_info.csv')


def load_data(nrows):
    data = pd.read_csv(DATA_URL, nrows=nrows, )
    return data


data_load_state = st.text('Loading data...')
data = load_data(10000)

data = data[data['spotify_id'].notnull()]

data_load_state.text(f"Loaded {len(data)} not null artists")

st.subheader('Raw data, len: ' + str(len(data)))
st.write(data['spotify_id'].head())

@st.cache(allow_output_mutation=True)
def spotify_client():
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials())

@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def artist_top_tracks(sp_artist_id):
    sp = spotify_client()

    results = sp.artist_top_tracks(sp_artist_id, country='RU')

    return results

st.subheader('Топ треков артиста по sp_id')
test_artist_sp_id = st.text_input('', '')
if test_artist_sp_id != '':
    st.write( artist_top_tracks(test_artist_sp_id) )


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_album(sp_album_id):
    sp = spotify_client()
    return sp.album(sp_album_id)

# @st.cache(suppress_st_warning=True, allow_output_mutation=True)
def get_artists_top_tracks(artists_sp_ids):
    sp_artists_top_tracks_data = pd.DataFrame({
        "artist_spotify_id": [],
        "name": [],
        "spotify_id": [],
        "duration_ms": [],
        "explicit": [],
        "popularity": [],
        "album_type": [],
        "album_name": [],
        "album_spotify_id": [],
        "release_date": [],
        "album_popularity": [],
        })

    curr_artist = st.text("")
    for artist_sp_id in StProgress(artists_sp_ids, title=f"Обкачиваем {len(artists_sp_ids)} артистов"):
        curr_artist.text = "curr artist " + artist_sp_id
        try:
            sp_artist_top_tracks = artist_top_tracks(artist_sp_id)

            for track in sp_artist_top_tracks['tracks']:
                sp_album = get_album(track['album']['id'])
                sp_artist_top_tracks_data = {
                    "artist_spotify_id":  artist_sp_id,
                    "name":  track['name'],
                    "spotify_id":  track['id'],
                    "duration_ms":  track['duration_ms'],
                    "explicit":  track['explicit'],
                    "popularity":  track['popularity'],
                    "album_type":  track['album']['album_type'],
                    "album_name":  track['album']['name'],
                    "album_spotify_id":  track['album']['id'],
                    "release_date":  track['album']['release_date'],
                    "album_popularity":  sp_album['popularity'],
                }
                sp_artists_top_tracks_data = sp_artists_top_tracks_data.append( sp_artist_top_tracks_data, ignore_index=True )

        except Exception as e:
            st.write(e)
            st.text("Some errors on processing artists on " + artist_sp_id)
            break

    return sp_artists_top_tracks_data


sp_artists_top_tracks_data = get_artists_top_tracks( data['spotify_id'] )

st.subheader("Итого")
st.write( sp_artists_top_tracks_data.head(50) )

sp_artists_top_tracks_data.to_csv("artist_top_tracks.csv")

st.subheader(f"Кол-во треков: {len(sp_artists_top_tracks_data)}")
