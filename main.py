import requests
from flask import Flask, request

app = Flask(__name__)


def parse_json(r):
    out = {
        "first_day": r["first_day_label"],
        "last_day": r["last_day_label"]
    }

    lezioni = []

    for lezione in r["celle"]:
        template_lezione = {
            "nome_insegnamento": lezione["nome_insegnamento"],
            "docente": lezione["docente"],
            "aula": lezione["aula"],
            "giorno": lezione["giorno"],
            "ora_inizio": lezione["ora_inizio"],
            "ora_fine": lezione["ora_fine"]
        }
        lezioni.append(template_lezione)

    out["lezioni"] = lezioni

    return out


def get_url():
    # codice anno di studio(Esempio: 2020)
    anno = request.args.get("anno")
    # codice corso di studio(Esempio: 420 )
    corso = request.args.get("corso")
    # codice anno di studio (Esempio: 999|2)
    anno2 = request.args.get("anno2")
    # data di cui interessa sapere le lezioni
    data = request.args.get("date")
    # anno di studio (Esempio: 1 - UNICO)
    txtcurr = request.args.get("txtcurr")
    url = f"https://logistica.univr.it/PortaleStudentiUnivr/grid_call.php?view=easycourse&include=corso&anno={anno}&corso={corso}&anno2[]={anno2}&visualizzazione_orario=cal&date={data}&&_lang=it&all_events=0&txtcurr={txtcurr}"
    return url


@app.route('/')
def main_roure():
    url = get_url()
    r = requests.get(url).json()
    r = parse_json(r)

    return r
