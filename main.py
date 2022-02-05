import squadre

import requests

def get_voti_live(giornata, codice_squadra, magic_number):
    url = f"https://www.fantacalcio.it/api/live/{codice_squadra}?g={giornata}&i={magic_number}"
    print(url)
    voti_live = requests.get(url)
    return voti_live.json()


# Voti live genoa
voti_roma = get_voti_live(giornata=24, codice_squadra=squadre.codici["Roma"], magic_number=16)
print(voti_roma)

voti_genoa = get_voti_live(giornata=24, codice_squadra=squadre.codici["Genoa"], magic_number=16)
print(voti_genoa)

voti_inter = get_voti_live(giornata=24, codice_squadra=squadre.codici["Inter"], magic_number=16)
print(voti_inter)

voti_milan = get_voti_live(giornata=24, codice_squadra=squadre.codici["Milan"], magic_number=16)
print(voti_milan)