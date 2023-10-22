import os
import json
import sys

from utils import (decode_protobuf_live_msg, get_protobuf_message_b64, get_voti,
                   get_signed_uri)
from squadre import codici

encoded = "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"


# Event ID -> str repr
event_mapper = {
   1: "ammonizione",
   2: "espulsione",
   3: "goal",
   4: "goal subito",
   9: "unknwon",  # ?
   11: "unknwon",  # maybe "goal decisivo" ?
   12: "unknwon",  # ?
   14: "sub out",
   15: "sub in",
   17: "unknown",  # ?
   20: "unknwon",  # ?
   21: "unknwon",  # ?
   22: "assist",
   23: "unknown",  # ?
   # Custom events
   99: "cleansheet",
}

# Apparently 55 is their designated magic number for SV
SV = 55

modmodulo = {}
modmodulo['P' + 4*'D' + 4*'C' + 2*'A'] = 0
modmodulo['P' + 3*'D' + 5*'C' + 2*'A'] = -0.5
modmodulo['P' + 4*'D' + 3*'C' + 3*'A'] = -1.0
modmodulo['P' + 3*'D' + 4*'C' + 3*'A'] = -1.5
modmodulo['P' + 5*'D' + 3*'C' + 2*'A'] = 0.5
modmodulo['P' + 4*'D' + 5*'C' + 1*'A'] = 1
modmodulo['P' + 5*'D' + 4*'C' + 1*'A'] = 1.5

strmodulo = {}
strmodulo['P' + 4*'D' + 4*'C' + 2*'A'] = '4-4-2'
strmodulo['P' + 3*'D' + 5*'C' + 2*'A'] = '3-5-2'
strmodulo['P' + 4*'D' + 3*'C' + 3*'A'] = '4-3-3'
strmodulo['P' + 3*'D' + 4*'C' + 3*'A'] = '3-4-3'
strmodulo['P' + 5*'D' + 3*'C' + 2*'A'] = '5-3-2'
strmodulo['P' + 4*'D' + 5*'C' + 1*'A'] = '4-5-1'
strmodulo['P' + 5*'D' + 4*'C' + 1*'A'] = '5-4-1'


"""
{
    "goal": 3,
    "assist": 1,
    "goal subito": -1,
    "ammonizione": -0.5,
    "espulsione": -1,
    "autogol": -1,
    "rigore segnato": 2,
    "rigore sbagliato": -1,
    "rigore parato": 3,
    "cleansheet": 1,
}
"""


script_directory = os.path.dirname(os.path.abspath(__file__))


def get_punteggi_lega():
    path = os.path.join(script_directory, 'data', 'punteggi.json')
    with open(path, 'r') as file:
        punteggi = json.load(file)

    punteggi['unknown'] = 0

    return punteggi


def get_ruoli_lega():
    path = os.path.join(script_directory, 'data', 'ruoli.txt')
    with open(path, 'r') as file:
        ruoli = file.readlines()

    mapper = {}
    for i in ruoli:
        # Expected format: ruolo, spaces, name, \n
        pos, name = i.replace("\n", "").split("\t")
        mapper[name] = pos

    return mapper


def get_squadre_serieA():
    path = os.path.join(script_directory, 'data', 'serieA.txt')
    with open(path, 'r') as file:
        serieA = file.readlines()

    mapper = {}
    for i in serieA:
        # Expected format: name, spaces, squadra (first three letters), \n
        name, squadra = i.replace("\n", "").split("\t")
        mapper[name] = squadra

    return mapper


def parse_fantasquadre():
    path = os.path.join(script_directory, 'data', 'formazioni')
    fantasquadre = []
    for filename in os.listdir(path):
        if filename.startswith('.'):
            continue

        file_path = os.path.join(path, filename)

        if os.path.isfile(file_path):
            with open(file_path, 'r') as f:
                content = f.read()
                fantasquadre.append(content)

    mapper = {}
    for i in fantasquadre:
        items = i.split("\n")

        # Sanitize (some hand-crafted files might include \t too)
        items = [j.replace("\t", "") for j in items]

        name = items[0]
        manager = items[1]
        titolari = {i: 0 for i in items[3:14]}  # giocatore -> voto
        panchinari = {i: 0 for i in items[15:-1]}

        mapper[name] = (titolari, panchinari)

    return mapper


def get_live_data():
    path = os.path.join(script_directory, 'data', 'giornata.txt')
    with open(path, 'r') as file:
        giornata = int(file.read())

    path = os.path.join(script_directory, 'data', 'voti_live.json')
    with open(path, 'r') as file:
        data_past = json.load(file)

    # TODO: CHECK ME LIVE!
    try:
        signed_uri = get_signed_uri(giornata, 18)
        encoded = get_protobuf_message_b64(signed_uri)
    except KeyError:
        encoded = ''

    data_live = decode_protobuf_live_msg(encoded[2:-1])

    # Merge past and live data
    data = {'protoData': (data_past.get('protoData', []) +
                          data_live.get('protoData', []))}

    return data


def inject_custom_events(data):
    matches = data['protoData']

    # Cleansheet event
    for match in matches:
        goalHome = match.get('goalHome', 0)
        goalAway = match.get('goalAway', 0)

        if goalHome == 0:
            for i in match['playersAway']:
                if i['position'] == 'P':
                    i.setdefault('events', []).append(99)
                    i.setdefault('eventsMinutes', []).append(120)  # Dummy min
        if goalAway == 0:
            for i in match['playersHome']:
                if i['position'] == 'P':
                    i.setdefault('events', []).append(99)
                    i.setdefault('eventsMinutes', []).append(120)  # Dummy min


def calc_voto_live(giocatore, punteggi):
    vote = giocatore['vote']
    events = giocatore.get('events', [])

    for event in events:
        try:
            event_name = event_mapper[event]
        except KeyError:
            raise RuntimeError("Unknown event `%d` for `%s`" % (event, giocatore))

        try:
            bonus_malus = punteggi[event_name]
        except KeyError:
            # E.g., sub out
            continue

        # We have the rule that SV+bonus_malus => 6+bonus_malus
        if vote == SV:
            vote = 6

        vote += bonus_malus

    if vote == 55:
        return 0
    else:
        return vote 


def calc_fantasquadra(titolari, panchinari, ruoli):
    tot = 0
    modulo = ""
    for name, voto in titolari.items():
        pos = ruoli[name]

        if voto == 0:
            # Perform sub
            for i in list(panchinari):
                subpos = ruoli[i]
                if subpos == pos:
                    voto = panchinari.pop(i)
                    pos = subpos
                    if voto != 0:
                        break

        tot += voto
        modulo += pos

    # Add modificatore squadra based on poss
    try:
        v = modmodulo[modulo]
    except KeyError:
        # Unknown player pos!
        v = 0
    tot += v

    return tot, strmodulo[modulo]


def purge():
    # Move tip to next matchday
    path = os.path.join(script_directory, 'data', 'giornata.txt')
    with open(path, 'r') as file:
        giornata = int(file.read())
    with open(path, 'w') as file:
        file.write("%s" % (giornata + 1))

    # Stash votes
    path = os.path.join(script_directory, 'data', 'voti_live.json')
    newpath = os.path.join(script_directory, 'data', 'voti_giornata_%d.json' % giornata)
    os.rename(path, newpath)

    # Recreate voti_live.json
    with open(path, 'w') as file:
        file.write("{}")

    with open(path, 'r') as file:
        data_ = json.load(file)


if __name__ == "__main__":
    # Launch: python matchday.py
    # Prerequisites:
    # * `punteggi.json` must be available
    # * `ruoli.txt` must be available
    # * `serieA.txt` must be available
    # * `formazioni/` must be available

    punteggi = get_punteggi_lega()
    ruoli = get_ruoli_lega()

    squadre = get_squadre_serieA()

    fantasquadre = parse_fantasquadre()

    if len(sys.argv) == 1:
        # Testing!
        data = decode_protobuf_live_msg(encoded)
    else:
        assert len(sys.argv) == 2
        if sys.argv[1] == 'live':
            data = get_live_data()
        elif sys.argv[1] == 'next':
            purge()
            sys.exit(0)
        else:
            raise ValueError

    inject_custom_events(data)

    unplayed = []
    for k, v in codici.items():
        serie_a_team = get_voti(data, v)

        if not serie_a_team:
            unplayed.append(k)
            continue

        for giocatore in serie_a_team:
            for team, (titolari, panchinari) in fantasquadre.items():
                name = giocatore['name']

                if name in titolari:
                    titolari[name] = calc_voto_live(giocatore, punteggi)
                elif name in panchinari:
                    panchinari[name] = calc_voto_live(giocatore, punteggi)
                else:
                    continue

    # Amend vote if player hasn't played yet
    for titolari_panchinari in fantasquadre.values():
        for m in titolari_panchinari:
            for name, vote in list(m.items()):
                if any(i.startswith(squadre[name]) for i in unplayed):
                    m[name] = 6  # S.V.

    output = {team: calc_fantasquadra(titolari, panchinari, ruoli)
              for team, (titolari, panchinari) in fantasquadre.items()}

    totali = {k: v for k, (v, _) in output.items()}
    table = sorted(totali, key=lambda i: output[i][0], reverse=True)

    print([(i, *output[i]) for i in table])
    # Nicely formatted output...
    # max_width = max(len(i) for i in totali)
    # for i in table:
    #     print(f"{i:>{max_width}} {totali[i]:.1f}")
