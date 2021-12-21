import json

import requests
from flask import Flask
from flask import request

from utils import Utils

app = Flask(__name__)


@app.route('/')
def main_roure():
    r = Utils.get_raw_json()
    r = Utils.parse_timetable(r)
    return r


@app.route('/universities')
def universities_route():
    available = ["Universita di Verona"]
    return json.dumps(available)


@app.route('/subjects')
def lessons_route():
    raw = Utils.get_raw_json()
    parsed_json = Utils.parse_lessons(raw)
    return parsed_json


@app.route('/years')
def get_years():
    url = "https://logistica.univr.it/PortaleStudentiUnivr/combo.php?sw=ec_&aa=1&_=1631535880476"
    result = requests.get(url).text
    years = Utils.get_years(result)
    return json.dumps(years)


@app.route('/courses')
def get_courses():
    url = Utils.get_courses_url()
    result = requests.get(url).text
    courses = Utils.get_courses(result)
    return json.dumps(courses)


@app.route('/v2/courses')
def get_courses_v2():
    url = Utils.get_courses_url()
    result = requests.get(url).text
    courses = Utils.get_courses_v2(result)
    return json.dumps(courses)


@app.route('/year2')
def get_year2():
    url = Utils.get_courses_url()
    course_id = request.args.get("corso")
    result = requests.get(url).text
    courses = Utils.get_years2(result, course_id)

    return json.dumps(courses)


if __name__ == "__main__":
    from waitress import serve

    serve(app, host="0.0.0.0", port=8080)
