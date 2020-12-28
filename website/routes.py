import json

from flask import render_template

from app import app
from map import prepare_regions, prepare_powiats_data
from courses import education_levels


@app.route('/')
def index():
    wojewodztwa = prepare_regions("static/maps/wojewodztwa-min.geojson")
    powiaty = prepare_regions("static/maps/powiaty-min.geojson")

    poland_west_most = 999
    poland_east_most = -999
    poland_north_most = -999
    poland_south_most = 999

    for wojewodztwo in wojewodztwa:
        poland_west_most = min(wojewodztwo["west_border"], poland_west_most)
        poland_east_most = max(wojewodztwo["east_border"], poland_east_most)
        poland_north_most = max(wojewodztwo["north_border"], poland_north_most)
        poland_south_most = min(wojewodztwo["south_border"], poland_south_most)

    poland_width = poland_east_most - poland_west_most
    poland_height = poland_north_most - poland_south_most

    powiats_data = json.dumps(prepare_powiats_data("static/maps/powiats.csv"))


    return render_template(
        "index.html",
        wojewodztwa=wojewodztwa,
        powiaty=powiaty,
        poland_west_most=poland_west_most,
        poland_north_most=poland_north_most,
        poland_width=poland_width,
        poland_height=poland_height,
        powiats_data=powiats_data
    )


@app.route('/form')
def form():
    courses = {
        level: [
            {
                'id': level + '_' + str(i),
                'label': course + ' (' + level + ')'
            }   
            for i, course in enumerate(courses_list)
        ]
        for level, courses_list in education_levels.items()
    }

    return render_template(
        "form.html",
        courses=courses
    )