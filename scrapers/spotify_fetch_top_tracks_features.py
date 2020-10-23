from typing import Any, Dict, List

import pandas as pd
import spotipy
import streamlit as st
from dotenv import load_dotenv
from spotipy.oauth2 import SpotifyClientCredentials

from scrapers.st_utils import StProgress

st.title("Spotify tracks features downloader")

DATA_URL = "../data/artist_top_tracks.csv"


def load_data(nrows: int) -> pd.DataFrame:
    data = pd.read_csv(
        DATA_URL,
        nrows=nrows,
    )
    return data


data_load_state = st.text("Loading data...")
data = load_data(None)

data_load_state.text(f"Loaded {len(data)} not null artists")

st.subheader("Raw data, len: " + str(len(data)))
st.write(data["spotify_id"].head())


@st.cache(allow_output_mutation=True)
def spotify_client() -> spotipy.client.Spotify:
    load_dotenv()
    return spotipy.Spotify(auth_manager=SpotifyClientCredentials())


@st.cache(suppress_st_warning=True, allow_output_mutation=True)
def track_features(sp_track_ids: List[str]) -> List[Dict[str, Any]]:
    sp = spotify_client()

    results = sp.audio_features(tracks=sp_track_ids)

    return results


st.subheader("Фичи трека по sp_id")
sp_track_id = st.text_input("", "")
if sp_track_id != "":
    st.write(track_features(sp_track_id))

st.write(data)


def get_tracks_features(sp_tracks_ids: List[str]) -> pd.DataFrame:

    batch_size = 10

    audio_features = [
        "key",
        "mode",
        "time_signature",
        "acousticness",
        "danceability",
        "energy",
        "instrumentalness",
        "liveness",
        "loudness",
        "speechiness",
        "valence",
        "tempo",
    ]
    sp_tracks_features = {k: [] for k in audio_features}
    for i in StProgress(
        range(0, len(sp_tracks_ids), batch_size),
        title=f"Обкачиваем {len(sp_tracks_ids)} артистов",
    ):

        try:
            sp_tracks_ids_batch = sp_tracks_ids[
                i : min(i + batch_size, len(sp_tracks_ids))
            ]
            tracks_features_list = track_features(sp_tracks_ids_batch)
            # print(tracks_features_list)
            for tr in tracks_features_list:
                for feature_name in audio_features:
                    if tr is not None:
                        sp_tracks_features[feature_name].append(tr[feature_name])
                    else:
                        sp_tracks_features[feature_name].append(None)

        except Exception as e:
            st.write(e)
            st.text("Some errors on processing artists on i=" + str(i))
            break

    return pd.DataFrame(sp_tracks_features)


sp_tracks_features = get_tracks_features(data["spotify_id"])

st.subheader("Итого")
st.write(len(data), len(sp_tracks_features))

data.reset_index(drop=True, inplace=True)
sp_tracks_features.reset_index(drop=True, inplace=True)

sp_tracks_features = pd.concat((data, sp_tracks_features), axis=1)

# приджойним имя артиста
artist_info = pd.read_csv("../data/artist_info.csv")
artist_info["artist"] = artist_info["name"]
artist_info = artist_info[["artist", "spotify_id"]]
artist_info.dropna(inplace=True)
artist_info.info()

sp_tracks_features = (
    sp_tracks_features.set_index("artist_spotify_id")
    .join(artist_info.set_index("spotify_id"))
    .reset_index()
)
sp_tracks_features.rename(columns={"index": "artist_spotify_id"}, inplace=True)

cols = sp_tracks_features.columns.tolist()
cols.insert(0, cols.pop(-1))
sp_tracks_features = sp_tracks_features[cols]

st.write(sp_tracks_features)

sp_tracks_features.to_csv("../data/artist_top_tracks_with_features.csv", index=False)

st.subheader(f"Кол-во треков: {len(sp_tracks_features)}")
