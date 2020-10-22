# Датасет с данными из Musicbrainz и Spotify о российских артистах и их лучших треках

## Данные об артистах

```
./artist_info.csv
```

### Структура и образцы данных

|      artist      |            musicbrainz_id            |       spotify_id       |  type  | followers |                                        genres                                        | popularity |
|:----------------:|:------------------------------------:|:----------------------:|:------:|:---------:|:------------------------------------------------------------------------------------:|:----------:|
| Shortparis       | e1f95266-0e43-4e25-9415-0596cb711d7b | 61j4FFbKlzdYihMtpM1hZD | Group  | 65521     | ["double drumming", "russian post-punk"]                                             | 46         |
| Порез на собаке  | 19743d1c-c537-477a-bf19-360824243b87 | 4DHJUKEpxQH7ypjFgXmAD6 | Group  | 4443      | ["russian indie"]                                                                    | 25         |
| П.Т.В.П.         | 671fcfd3-54c4-4b76-ac23-999a606f1f0c | 3lWr0BTSW10qY5fajZjKSK | Group  | 15255     | ["russian punk", "russian rock"]                                                     | 33         |
| ВСИГМЕ           | 2483f29e-127b-44b5-8c15-c402b85c1660 | 5f6SoqrMsA8Rb4NuSnsgaj | Group  | 423       | []                                                                                   | 11         |
| Сергей Прокофьев | 0e43fe9d-c472-4b62-be9e-55f971a023e1 | 4kHtgiRnpmFIV5Tm4BIs8l | Person | 167015    | ["classical", "early modern classical", "neoclassicism", "russian modern classical"] | 58         |

#### Описание полей в таблице

| Поле             | Тип    | Описание                                                               |
|------------------|--------|------------------------------------------------------------------------|
| `artist`         | `str`  | имя артиста или название группы                                        |
| `musicbrainz_id` | `str`  | уникальный идентификатор артиста в музыкальной базе данных Musicbrainz |
| `spotify_id`     | `str`  | уникальный идентификатор артиста в стриминговом сервисе Spotify        |
| `type`           | `str`  | тип исполнителя, может принимать значения `Person` или `Group`         |
| `followers`      | `int`  | количество подписчиков артиста на Spotify                              |
| `genres`         | `list` | музыкальные жанры артиста                                              |
| `popularity`     | `int`  | индекс популярности артиста на Spotify *                               |

\* Может принимать значения от 0 до 100, где 100 означает самую высокую популярность. Рассчитывается на основе популярности всех треков артиста.

### Источники данных

Поля `artist`, `musicbrainz_id` и `type` извлекаем из музыкальной базы данных Musicbrainz, так как там есть возможность получить список артистов связанных с одной страной.
Извлечь эти данные можно двумя способами:
1. Постранично парсить раздел Artists на странице с информацией о России: https://musicbrainz.org/area/1f1fc3a4-9500-39b8-9f10-f0a465557eef/artists?page=1
2. Достать данные через API
    - Ссылки на документацию
        - https://musicbrainz.org/doc/MusicBrainz_API
        - https://musicbrainz.org/doc/MusicBrainz_API/Search
    - Пример запроса
        - `GET` на http://musicbrainz.org/ws/2/artist/?query=area:russia&fmt=json&offset=0&limit=100
        
Остальные поля получаем в результате `GET` запросов к эндпоинту `https://api.spotify.com/v1/search` Spotify API.
При отправке запроса в значении параметра `q` указываем имя артиста, а в значении параметра `type` указываем `artist`. \
Ссылка на документацию: https://developer.spotify.com/documentation/web-api/reference/search/search/


## Данные о лучших треках

```
./artist_top_tracks_with_features.csv
```

### Структура и образцы данных

|      artist      |    artist_spotify_id   |                                            name                                            |       spotify_id       | duration_ms | explicit | popularity | album_type |          album_name         |    album_spotify_id    | release_date | album_popularity | key | mode | time_signature | acousticness | danceability | energy | instrumentalness | liveness | loudness | speechiness | valence |  tempo  |
|:----------------:|:----------------------:|:------------------------------------------------------------------------------------------:|:----------------------:|:-----------:|:--------:|:----------:|:----------:|:---------------------------:|:----------------------:|:------------:|:----------------:|:---:|:----:|:--------------:|:------------:|:------------:|:------:|:----------------:|:--------:|:--------:|:-----------:|:-------:|:-------:|
| Shortparis       | 61j4FFbKlzdYihMtpM1hZD | Страшно                                                                                    | 5vbX1g08j9hGzW93CAIeQo | 289682      | false    | 48         | album      | Так закалялась сталь        | 4RSGIq9Yu5i70lfXJQ19px | 2019-11-01   | 48               | 11  | 0    | 3              | 0.00861      | 0.62         | 0.822  | 0.633            | 0.085    | -7.434   | 0.0385      | 0.451   | 117.005 |
| Порез на собаке  | 4DHJUKEpxQH7ypjFgXmAD6 | У Пожара Внутри                                                                            | 2X0wU5wniSmslkpN4raRWu | 338801      | false    | 21         | album      | Горе Поводырь               | 2uZq9bcewcaKRGQOGlnIzR | 2016         | 22               | 4   | 0    | 1              | 0.316        | 0.376        | 0.337  | 0.000602         | 0.364    | -12.425  | 0.0471      | 0.0591  | 129.461 |
| П.Т.В.П.         | 3lWr0BTSW10qY5fajZjKSK | В нирване                                                                                  | 1W4jYmQBjXtuZW0qAjVg2S | 117353      | false    | 33         | album      | Гексаген                    | 62WvNAwN8JJOHOlDswU7H8 | 2001-01-01   | 30               | 0   | 1    | 4              | 0.00204      | 0.601        | 0.846  | 0.0000867        | 0.134    | -7.493   | 0.0392      | 0.846   | 128.698 |
| ВСИГМЕ           | 5f6SoqrMsA8Rb4NuSnsgaj | Балконы                                                                                    | 798iNswoND89ZPdBLY6GCl | 240733      | false    | 8          | album      | Река                        | 1ySZBaUjbj3PjVnea7sJnt | 2017-08-10   | 11               | 1   | 1    | 4              | 0.184        | 0.83         | 0.731  | 0                | 0.131    | -5.418   | 0.136       | 0.365   | 121.977 |
| Сергей Прокофьев | 4kHtgiRnpmFIV5Tm4BIs8l | Prokofiev: Romeo and Juliet, Op. 64, Act 1: No. 13, Dance of the Knights (Complete Ballet) | 7HSs4srn1qnZhh7WRWBVOk | 341693      | false    | 56         | album      | Prokofiev: Romeo and Juliet | 3M5idfqFUxge3skgZQu4R3 | 1973         | 52               | 0   | 1    | 4              | 0.927        | 0.209        | 0.101  | 0.9              | 0.0776   | -19.383  | 0.0403      | 0.153   | 85.851  |

#### Описание полей в таблице

##### Информация о треке

| Поле                | Тип    | Описание                                                                                                                                                 |
|---------------------|--------|----------------------------------------------------------------------------------------------------------------------------------------------------------|
| `artist_spotify_id` | `str`  | уникальный идентификатор артиста в стриминговом сервисе Spotify (по нему можно будет джойнить таблицы, так как это  `spotify_id` из таблицы с артистами) |
| `artist`            | `str`  | имя артиста или название группы                                                                                                                          |
| `name`              | `str`  | название трека                                                                                                                                           |
| `spotify_id`        | `str`  | уникальный идентификатор трека в стриминговом сервисе Spotify                                                                                            |
| `duration_ms`       | `int`  | длительность трека в миллисекундах                                                                                                                       |
| `explicit`          | `bool` | содержит ли текст трека нецензурные выражения, может принимать значения  `true`  или  `false`                                                             |
| `popularity`        | `int`  | индекс популярности трека на Spotify *                                                                                                                   |
| `album_type`        | `str`  | тип альбома, может принимать значения  `album`  ,  `single`  или  `compilation`                                                                          |
| `album_name`        | `str`  | название альбома                                                                                                                                         |
| `album_spotify_id`  | `str`  | уникальный идентификатор альбома в стриминговом сервисе Spotify                                                                                          |
| `release_date`      | `str`  | дата выхода альбома                                                                                                                                      |
| `album_popularity`  | `int`  | индекс популярности альбома на Spotify *                                                                                                                 |

\* Может принимать значения от 0 до 100, где 100 означает самую высокую популярность. Популярность трека рассчитывается специальным алгоритмом Spotify 
на основе количества прослушиваний трека и на том, как недавно они произошли. Популярность альбома рассчитывается на основе популярности его треков.

##### Особенности аудио

Каждый параметр подробно описан в документации к API Spotify: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/

| Поле               | Тип     | Описание                                                                                                                           |
|--------------------|---------|------------------------------------------------------------------------------------------------------------------------------------|
| `key`              | `int`   | предполагаемая общая тональность трека, целые числа накладываются на нотацию звуковысотных классов, 0 = C, 1 = C♯/D♭, 2 = D и т.д. |
| `mode`             | `int`   | указывает модальность трека, мажор -1, минор - 0                                                                                   |
| `time_signature`   | `int`   | предполагаемый общий тактовый размер композиции                                                                                    |
| `acousticness`     | `float` | мера достоверности от 0.0 до 1.0 того, является ли трек акустическим                                                               |
| `danceability`     | `float` | описывает, насколько трек подходит для танцев от 0.0 до 1.0                                                                        |
| `energy`           | `float` | представляет собой перцептивную меру интенсивности и активности от 0.0 до 1.0                                                      |
| `instrumentalness` | `float` | определяет, содержит ли трек вокал, принимает значения от 0.0 до 1.0                                                               |
| `liveness`         | `float` | определяет присутствие аудитории при записи, принимает значения от 0.0 до 1.0                                                      |
| `loudness`         | `float` | общая громкость трека в децибелах, типичный диапазон значений от -60 до 0 дБ                                                       |
| `speechiness`      | `float` | определяет наличие произнесенных слов в треке, принимает значения от 0.0 до 1.0                                                    |
| `valence`          | `float` | описывает музыкальную "позитивность", передаваемую треком, принимает значения от 0.0 до 1.0                                        |
| `tempo`            | `float` | предполагаемый общий темп трека в ударах в минуту                                                                                  |

### Источники данных

Поля `name`, `spotify_id`, `duration_ms`, `explicit`, `popularity`, `album_type`, `album_name`, `album_spotify_id`, `release_date` 
получаем с помощью `GET` запроса на `https://api.spotify.com/v1//v1/artists/{id}/top-tracks`, 
указывая в качестве значения параметра `id` Spotify ID артиста, который мы получили ранее, 
а в значении параметра `market` указываем `RU`. \
Ссылка на документацию: https://developer.spotify.com/documentation/web-api/reference/artists/get-artists-top-tracks/

Поле `album_popularity` можно получить, сделав `GET` запрос на `https://api.spotify.com/v1/albums/{id}`, указав `album_spotify_id`, полученный ранее, в качестве значения для параметра `id`. \
Ссылка на документацию: https://developer.spotify.com/documentation/web-api/reference/albums/get-album/

Получить особенности аудио можно двумя способами:
1. Для получения данных об одном треке нужно сделать `GET` запрос на `https://api.spotify.com/v1/audio-features/{id}`, указав его Spotify ID как значение параметра `id`. \
Ссылка на документацию: https://developer.spotify.com/documentation/web-api/reference/tracks/get-audio-features/
2. Чтобы получить данные о нескольких треках сразу, отправляем `GET` запрос на `https://api.spotify.com/v1/audio-features`, передавая Spotify ID этих треков через запятую как значение для параметра `ids`. \
Ссылка на документацию: https://developer.spotify.com/documentation/web-api/reference/tracks/get-several-audio-features/


## Скрипты

| Скрипт | Задача |
| -- | -- |
| `musicbrainz_get_artists.py` | Обкачка артистов с musicbrainz |
| `spotify_fetch_artist_info.py` | Обкачка артистов с spotify |
| `spotify_fetch_artist_top_tracks.py` | Обкачка топов треков со spotify |
| `spotify_fetch_top_tracks_features.py` | Обкачка фичей для треков со spotify |

<!-- todo add requrements.txt -->