import json
import time
import squadre
import requests
import schedule
import argparse

def request_voti_live(giornata, codice_squadra, magic_number):
    url = f"https://www.fantacalcio.it/api/live/{codice_squadra}?g={giornata}&i={magic_number}"
    response = requests.get(url, timeout=10)
    json_resp = response.json()
    json_resp_time = {
        "voti": json_resp,
        "timestamp": round(time.time())
    }
    return json_resp_time


def save_json(filename, voti_live):
    with open(filename, "w") as f:
        json.dump(voti_live, f, indent=4)


def cli_args():
    parser = argparse.ArgumentParser(
        usage="%(prog)s",
        description="Record voti live"
    )

    parser.add_argument("--squadra", dest="squadra", type=str)
    parser.add_argument("--giornata", dest="giornata", type=int)
    parser.add_argument("--magic", dest="magic", type=int, default=16)
    parser.add_argument("--until", dest="until", type=str)

    return parser.parse_args()


def task(giornata, squadra, magic):
    print(time.localtime())
    
    voti = request_voti_live(giornata=giornata, codice_squadra=squadre.codici[squadra], magic_number=magic)

    filename = f"{squadra}_{giornata}_{voti['timestamp']}.json"
    save_json(filename, voti)


if __name__ == "__main__":
    args = cli_args()
    print(f"Squadra: {args.squadra}")
    print(f"Giornata: {args.giornata}")
    print(f"Until: {args.until}")

    print(f"Start @ {time.localtime()}")

    schedule.every(30).seconds.until(args.until).do(
        task, args.giornata, args.squadra, args.magic)

    while True:
        schedule.run_pending()
        time.sleep(1)