import requests

def execute_search(user_search):

    raw_results = send_request(user_search)
    track_list = parse_results(raw_results)

    return track_list

def send_request(user_search):
    url = 'http://api.spotify.com/v1/search?q={0}&type=track&limit=35'
    user_search = '+'.join(user_search.split())

    final_url = url.format(user_search)
    raw_results = requests.get(final_url)

    return raw_results.json()

def parse_results(target_json):
    track_list = []

    for index, item in enumerate(target_json['tracks']['items'], start=1):
        song_name = item['name']
        artist = item['artists'][0]['name']
        album_name = item['album']['name']

        track_list.append((index, song_name, artist, album_name, item['uri']))

    return track_list

