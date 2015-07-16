import requests

def execute_search(user_search):

    raw_results = search_request(user_search)
    track_list = parse_search_results(raw_results)

    return track_list

def search_request(user_search):
    url = 'http://api.spotify.com/v1/search?q={0}&type=track&limit=35'
    user_search = '+'.join(user_search.split())

    url  = url.format(user_search)
    raw_results = requests.get(url)

    return raw_results.json()

def parse_search_results(target_json):
    track_list = []

    for index, item in enumerate(target_json['tracks']['items']):
        song_name = item['name']
        artist = item['artists'][0]['name']
        album_name = item['album']['name']
        song_uri = item['uri']
        artist_uri = item['artists'][0]['uri']
        album_uri = item['album']['uri']
        artist_id = item['artists'][0]['id']
        album_id = item['album']['id']

        track_list.append((index, song_name, artist, album_name, song_uri, artist_uri, album_uri, artist_id, album_id))

    return track_list

def get_artist_top(artist_id, country_id):

    raw_results = artist_request(artist_id, county_id)
    track_list = parse_artist_top_results(raw_results)

    return track_list

def artist_request(artist_id, country_id):
    url = 'https://api.spotify.com/v1/artists/{0}/top-tracks?country={1}'.format(artist_id, country_id)
    raw_results = requests.get(url)

    return raw_results.json()

def parse_artist_top_results(target_json):
    track_list = []

    for index, item in enumerate(target_json['tracks']):
        song_name = item['name']
        artist = item['artists'][0]['name']
        album_name = item['album']['name']
        song_uri = item['uri']
        album_uri = item['album']['uri']
        artist_uri = item['artists'][0]['uri']
        artist_id = item['artists'][0]['id']
        album_id = item['album']['id']
        track_list.append((index, song_name, artist, album_name, song_uri, album_uri, artist_uri, artist_id, album_id))

    return track_list

def get_album_tracks(album_id):

    raw_results = album_request(album_id)
    track_list = parse_album_results(raw_results)

    return track_list

def album_request(album_id):
    url = 'https://api.spotify.com/v1/albums/{0}/tracks'.format(album_id)
    raw_results = requests.get(url)

    return raw_results

def parse_album_results(target_json):

    track_list = []

    for index, item in enumerate(target_json['items']):
        song_name = item['name']
        artist = item['artists'][0]['name']
        album_name = item['album']['name']
        song_uri = item['uri']
        album_uri = item['album']['uri']
        artist_uri = item['artists'][0]['uri']
        artist_id = item['artists'][0]['id']
        album_id = item['album']['id']

        track_list.append((index, song_name, artist, album_name, song_uri, album_uri, artist_uri, artist_id, album_id))

    return track_list
