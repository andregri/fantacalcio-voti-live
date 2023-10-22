import base64
import requests
import os
import subprocess
import json

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


def decode_protobuf_live_msg(encoded_msg):
    script_directory = os.path.dirname(os.path.abspath(__file__))
    decode_livemessage_pb = os.path.join(script_directory, 'decode_livemessage_pb.js')
    p = subprocess.Popen(['node', decode_livemessage_pb, encoded_msg], stdout=subprocess.PIPE)
    out = p.stdout.read()
    return json.loads(out.decode())


def get_voti(data_json, codice_squadra):
    matches = data_json['protoData']
    for match in matches:
        if match['teamIdHome'] == codice_squadra:
            return match['playersHome']
        elif match['teamIdAway'] == codice_squadra:
            return match['playersAway']
    return dict()


if __name__ == "__main__":
    data_b64 = get_protobuf_message_b64(get_signed_uri(9,18))
    data = decode_protobuf_live_msg(data_b64[2:-1])
    json_object = json.dumps(data, indent = 4) 
    print(json_object)
