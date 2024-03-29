import json
import time
import squadre
import requests
import schedule
import argparse
import db
from datetime import datetime
import utils

cache_giocatori = {} # key: id giocatore
cache_voto = {} # key: id giocatore

def now():
    # datetime object containing current date and time
    time = datetime.now()

    # dd/mm/YY H:M:S
    return time.strftime("%m/%d/%Y %H:%M:%S")


def request_voti_live(giornata, codice_squadra, magic_number):
    signed_uri = utils.get_signed_uri(giornata, season_id=18)
    msg_b64 = utils.get_protobuf_message_b64(signed_uri)
    msg_b64 = msg_b64[2:-1] # remove "b'" at the beginning and trailing "'"
    all_data = utils.decode_protobuf_live_msg(msg_b64)
    json_resp = utils.get_voti(all_data, codice_squadra)
    json_resp_time = {
        "voti": json_resp,
        "timestamp": now()
    }
    return json_resp_time


def save_json(filename, voti_live):
    with open(filename, "w") as f:
        json.dump(voti_live, f, indent=4)


def store_giocatore(giocatore):
    db.store_giocatore(giocatore)
    cache_giocatori[giocatore.id] = giocatore


def store_voto(voto):
    db.store_voto(voto)
    cache_voto[voto.id_giocatore] = voto


def cli_args():
    parser = argparse.ArgumentParser(
        usage="%(prog)s",
        description="Record voti live"
    )

    parser.add_argument('squadre', metavar='squadre', type=str, nargs='+', 
                        help='squadre to be monitored')
    parser.add_argument("--giornata", dest="giornata", type=int)
    parser.add_argument("--magic", dest="magic", type=int, default=16)
    parser.add_argument("--until", dest="until", type=str)

    return parser.parse_args()


def task(giornata, squadra, magic):
    print(f"{squadra} {now()}")
    
    try:
        resp = request_voti_live(giornata=giornata, codice_squadra=squadre.codici[squadra], magic_number=magic)
    except Exception as e:
        print(e)
    else:
        for el in resp["voti"]:
            # create objects from json response
            giocatore = db.Giocatore(el["id"], el["name"], el["position"], squadra)
            voto = db.Voto(el["id"], giornata, el["vote"], el.get("events"), resp["timestamp"])

            # compare giocatore to cache
            if not giocatore.id in cache_giocatori:
                store_giocatore(giocatore)

            # compare voto to cache
            if not voto.id_giocatore in cache_voto:
                store_voto(voto)
            else:
                if cache_voto[voto.id_giocatore] != voto:
                    store_voto(voto)


if __name__ == "__main__":
    args = cli_args()
    print(f"Squadre: {args.squadre}")
    print(f"Giornata: {args.giornata}")
    print(f"Until: {args.until}")

    print(f"Start @ {now()}")

    db.init_tables()

    for squadra in args.squadre:
        schedule.every(30).seconds.until(args.until).do(
            task, args.giornata, squadra, args.magic)

    while True:
        schedule.run_pending()
        time.sleep(1)
