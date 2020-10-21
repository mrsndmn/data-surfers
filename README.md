# Датасет с данными из Musicbrainz и Spotify о российских артистах и их лучших треках

## Данные об артистах

### Структура и образцы данных

|      artist      |            musicbrainz_id            |       spotify_id       |  type  | followers |                                        genres                                        | popularity |
|:----------------:|:------------------------------------:|:----------------------:|:------:|:---------:|:------------------------------------------------------------------------------------:|:----------:|
| Shortparis       | e1f95266-0e43-4e25-9415-0596cb711d7b | 61j4FFbKlzdYihMtpM1hZD | Group  | 65521     | ["double drumming", "russian post-punk"]                                             | 46         |
| Порез на собаке  | 19743d1c-c537-477a-bf19-360824243b87 | 4DHJUKEpxQH7ypjFgXmAD6 | Group  | 4443      | ["russian indie"]                                                                    | 25         |
| П.Т.В.П.         | 671fcfd3-54c4-4b76-ac23-999a606f1f0c | 3lWr0BTSW10qY5fajZjKSK | Group  | 15255     | ["russian punk", "russian rock"]                                                     | 33         |
| ВСИГМЕ           | 2483f29e-127b-44b5-8c15-c402b85c1660 | 5f6SoqrMsA8Rb4NuSnsgaj | Group  | 423       | []                                                                                   | 11         |
| Сергей Прокофьев | 0e43fe9d-c472-4b62-be9e-55f971a023e1 | 4kHtgiRnpmFIV5Tm4BIs8l | Person | 167015    | ["classical", "early modern classical", "neoclassicism", "russian modern classical"] | 58         |

- `artist` - имя артиста или название группы
- `musicbrainz_id` - уникальный идентификатор артиста в музыкальной базе данных Musicbrainz
- `spotify_id` - уникальный идентификатор артиста в стриминговом сервисе Spotify
- `type` - тип исполнителя (персона или группа)
- `followers` - количество подписчиков на Spotify
- `genres` - музыкальные жанры артиста
- `popularity` - индекс популярности артиста на Spotify *

\* значения от 0 до 100, где 100 означает самую высокую популярность. Рассчитывается на основе популярности всех треков артиста.

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
