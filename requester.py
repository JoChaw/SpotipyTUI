import requests

def execute_search(user_search):

    raw_results = send_request(user_search)
    track_list = parse_results(raw_results)

def send_request(user_search):
    url = 'http://api.spotify.com/v1/search?q={0}&type&limit=35'
    user_search = '+'.join(user_search.split())

    final_url = url.format(user_search)
    raw_results = requests.get(final_url)

    return raw_results

def parse_results(target_json):

