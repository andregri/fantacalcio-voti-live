import base64
import requests

def get_signed_uri(giornata, season_id=18):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Content-Type': 'application/json',
        'Origin': 'https://www.fantacalcio.it',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-origin',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    uri = f'https://api.fantacalcio.it/v1/st/{season_id}/matches/live/{giornata}.dat'
    json_data = {
        'resourcesUri': [
            uri,
        ],
    }

    response = requests.post('https://www.fantacalcio.it/api/v1/SignedUri', headers=headers, json=json_data)
    
    if response.status_code == 200:
        return response.json()[uri]['resources'][0]['signedUri']


def get_protobuf_message_b64(signed_uri):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/117.0',
        'Accept': '*/*',
        'Accept-Language': 'en-GB,en;q=0.5',
        # 'Accept-Encoding': 'gzip, deflate, br',
        'Referer': 'https://www.fantacalcio.it/',
        'Content-Type': 'application/json',
        'Origin': 'https://www.fantacalcio.it',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Sec-Fetch-Dest': 'empty',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Site': 'same-site',
        # 'If-Modified-Since': 'Sun, 17 Sep 2023 16:54:15 GMT',
        # 'If-None-Match': 'W/"b09a890c5491cfcca3ecb5efb0533713"',
        'Cache-Control': 'max-age=0',
        # Requests doesn't support trailers
        # 'TE': 'trailers',
    }

    params = {}

    response = requests.get(signed_uri, params=params, headers=headers)

    return str(base64.b64encode(response.content))

data_b64 = get_protobuf_message_b64(get_signed_uri(4,18))
print(data_b64)