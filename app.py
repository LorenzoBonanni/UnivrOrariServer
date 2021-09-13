import json

import requests
from flask import Flask, request

app = Flask(__name__)


def parse_timetable(r):
    out = {
        "first_day": r["first_day_label"],
        "last_day": r["last_day_label"]
    }

    lezioni = []

    for lezione in r["celle"]:
        try:
            template_lezione = {
                "nome_insegnamento": lezione["nome_insegnamento"],
                "docente": lezione["docente"],
                "aula": lezione["aula"],
                "giorno": lezione["giorno"],
                "ora_inizio": lezione["ora_inizio"],
                "ora_fine": lezione["ora_fine"]
            }
            lezioni.append(template_lezione)
        except KeyError:
            continue

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
    url = f"https://logistica.univr.it/PortaleStudentiUnivr/grid_call_new.php?view=easycourse&form-type=corso&include=corso&txtcurr=&anno={anno}&corso={corso}&anno2%5B%5D={anno2}&visualizzazione_orario=cal&date={data}&periodo_didattico=&_lang=it&list=0&week_grid_type=-1&ar_codes_=&ar_select_=&col_cells=0&empty_box=0&only_grid=0&highlighted_date=0&all_events=0&faculty_group=0&_lang=it&all_events=0&txtcurr={txtcurr}"
    return url


def get_courses_url():
    # codice anno di studio(Esempio: 2020)
    anno = request.args.get("anno")
    url = f"https://logistica.univr.it/PortaleStudentiUnivr/combo.php?sw=ec_&aa={anno}&page=corsi&_=1631551434382"
    return url

def parse_lessons(r):
    out = {}
    legenda = r["legenda"]
    out["lezioni"] = [l['nome'] for l in legenda]
    return out


def get_raw_json():
    url = get_url()
    r = requests.get(url).json()
    return r


@app.route('/')
def main_roure():
    r = get_raw_json()
    r = parse_timetable(r)
    return r


@app.route('/subjects')
def lessons_route():
    r = get_raw_json()
    r = parse_lessons(r)
    return r


@app.route('/years')
def get_years():
    url = "https://logistica.univr.it/PortaleStudentiUnivr/combo.php?sw=ec_&aa=1&_=1631535880476"
    r = requests.get(url).text
    r = r.split(" = ")[1]
    r = r[:-1]
    years = eval(r)
    years = [[v["label"], k] for k, v in years.items()]
    return json.dumps(years)


@app.route('/courses')
def get_courses():
    url = get_courses_url()
    result = requests.get(url).text.split("\n")[0].split(" = ")[1][:-1]
    result = eval(result)
    corsi = [
        [
            e["label"],
            e["valore"],
            [
                {"label": e2["label"],
                 "valore": e2['valore']
                 } for e2 in e["elenco_anni"]
            ]
        ] for e in result
    ]

    return json.dumps(corsi)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
