import json
import time
import squadre
import requests
import schedule

def request_voti_live(giornata, codice_squadra, magic_number):
    url = f"https://www.fantacalcio.it/api/live/{codice_squadra}?g={giornata}&i={magic_number}"
    print(url)
    response = requests.get(url, timeout=10)
    json_resp = response.json()
    json_resp_time = {
        "voti": json_resp,
        "timestamp": round(time.time())
    }
    return json_resp_time


def save_json(voti_live):
    with open(f"resp_{voti_live['timestamp']}.json", "w") as f:
        json.dump(voti_live, f, indent=4)


if __name__ == "__main__":
    voti_milan = request_voti_live(giornata=24, codice_squadra=squadre.codici["Milan"], magic_number=16)
    save_json(voti_milan)
    #schedule.every(3).seconds.do(request_voti_live, giornata=24, codice_squadra=squadre.codici["Inter"], magic_number=16)
#
    #while True:
    #    schedule.run_pending()
    #    time.sleep(1)