import requests
import pandas as pd
import time

def MB_get_artists(limit, offset=0):
    """
    Функция принимает на вход лимит(сколько пользователей нужно получить),
    делает запрос по API Musicbrainz,
    и выдаёт на выходе список российских артистов с полями: ["id", "type", "score", "name"]
    """
    data = [] # итоговый лист
    while limit >= 0:
        request = requests.get(url="https://musicbrainz.org/ws/2/artist", params={"query":"area:russia","fmt":"json","offset":offset,"limit":100})
        json_data = request.json()["artists"]
        print(abs(offset/100), end=" ")
        offset += 100
        limit -= 100
        for artist in json_data:
            sample = [artist.get(key) for key in ["id", "type", "score", "name"]]
            data.append(sample)
        time.sleep(0.5)
    df = pd.DataFrame(data, columns=['musicbrainz_id', 'type', 'score', 'name'])
    df = df.drop_duplicates(subset=["name"])
    return df


if __name__ == "__main__":
    data = MB_get_artists(15000)
    data.to_csv("musicbrainz_artists", index=False)
