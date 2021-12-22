import requests
from flask import request


class Utils:
    @staticmethod
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

    @staticmethod
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
        return f"https://logistica.univr.it/PortaleStudentiUnivr/grid_call_new.php?view=easycourse&form-type=corso&include=corso&txtcurr=&anno={anno}&corso={corso}&anno2%5B%5D={anno2}&visualizzazione_orario=cal&date={data}&periodo_didattico=&_lang=it&list=0&week_grid_type=-1&ar_codes_=&ar_select_=&col_cells=0&empty_box=0&only_grid=0&highlighted_date=0&all_events=0&faculty_group=0&_lang=it&all_events=0&txtcurr={txtcurr}"

    @staticmethod
    def get_courses_url():
        # codice anno di studio(Esempio: 2020)
        anno = request.args.get("anno")
        url = f"https://logistica.univr.it/PortaleStudentiUnivr/combo.php?sw=ec_&aa={anno}&page=corsi&_=1631551434382"
        return url

    @staticmethod
    def parse_lessons(r):
        out = {}
        legenda = r["legenda"]
        out["lezioni"] = [l['nome'] for l in legenda]
        return out

    @staticmethod
    def get_raw_json():
        """
        makes a get request to the url and then return the obtained json
        :return:
        """
        url = Utils.get_url()
        response = requests.get(url).json()
        print(type(response))
        return response

    @staticmethod
    def get_years(text: str):
        result = text.split(" = ")[1]
        result = result[:-1]
        years = eval(result)
        years = [[v["label"].replace("\/", "/"), k] for k, v in years.items()]
        return years

    @staticmethod
    def get_courses(text: str):
        result = text.split("\n")[0].split(" = ")[1][:-1]
        result = eval(result)
        courses = [
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
        return courses

    @staticmethod
    def get_courses_v2(text: str):
        result = text.split("\n")[0].split(" = ")[1][:-1]
        result = eval(result)
        courses = [
            [e["label"], e["valore"]] for e in result
        ]

        return courses

    @staticmethod
    def get_years2(text: str, id: str):
        result = text.split("\n")[0].split(" = ")[1][:-1]
        result = eval(result)
        courses = {
            e["valore"]: {
                [e2["label"], e2['valore']] for e2 in e["elenco_anni"]
            }
            for e in result
        }

        return courses[id]
