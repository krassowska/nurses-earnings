import json

from flask import render_template

from app import app
from map import prepare_regions, prepare_powiats_data


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
    specjalizacje = [
        'Pielęgniarstwo anestezjologiczne i intensywnej opieki',
        'Pielęgniarstwo chirurgiczne',
        'Pielęgniarstwo geriatryczne',
        'Pielęgniarstwo internistyczne',
        'Pielęgniarstwo onkologiczne',
        'Pielęgniarstwo operacyjne',
        'Pielęgniarstwo opieki długoterminowej',
        'Pielęgniarstwo opieki paliatywnej',
        'Pielęgniarstwo pediatryczne',
        'Pielęgniarstwo psychiatryczne',
        'Pielęgniarstwo ratunkowe',
        'Pielęgniarstwo rodzinne',
        'Ochrona zdrowia pracujących',
        'Pielęgniarstwo epidemiologiczne',
        'Pielęgniarstwo neonatologiczn',
        'Pielęgniarstwo ginekologiczno-położnicze',
        'Pielęgniarstwo rodzinne'
    ]
    kursy_kwalifikacyjne = [
        'Pielęgniarstwo anestezjologiczne i intensywnej opieki',
        'Pielęgniarstwo chirurgiczne',
        'Pielęgniarstwo diabetologiczne',
        'Pielęgniarstwo geriatryczne',
        'Pielęgniarstwo internistyczne',
        'Pielęgniarstwo kardiologiczne',
        'Pielęgniarstwo nefrologiczne z dializoterapią',
        'Pielęgniarstwo neonatologiczne',
        'Pielęgniarstwo neurologiczne',
        'Pielęgniarstwo onkologiczne',
        'Pielęgniarstwo operacyjne',
        'Pielęgniarstwo opieki długoterminowej',
        'Pielęgniarstwo opieki paliatywnej',
        'Pielęgniarstwo pediatryczne',
        'Pielęgniarstwo psychiatryczne',
        'Pielęgniarstwo ratunkowe',
        'Pielęgniarstwo rodzinne',
        'Pielęgniarstwo środowiska nauczania i wychowania',
        'Pielęgniarstwo transplantacyjne',
        'Ochrona zdrowia pracujących',
        'Pielęgniarstwo epidemiologiczne',
        'Pielęgniarstwo anestezjologiczne i intensywnej opieki w położnictwie i ginekologii',
        'Pielęgniarstwo operacyjne',
        'Pielęgniarstwo rodzinne'
    ]

    kursy_specjalistyczne = [
        'Dializoterapia',
        'Endoskopia',
        'Kompleksowa opieka pielęgniarska w schorzeniach narządu wzroku',
        'Kompresjoterapia',
        'Leczenie ran',
        'Opieka nad dzieckiem z chorobą nowotworową',
        'Opieka nad dziećmi i młodzieżą z cukrzycą',
        'Opieka nad dziećmi ze schorzeniami otorynolaryngologicznymi',
        'Opieka nad pacjentem poddawanym proc. diag. i terap. z użyciem otwartych źródeł promieniowania',
        'Opieka nad pacjentem z przewlekłą obturacyjną chorobą płuc (POChP)',
        'Opieka nad pacjentem ze stomią jelitową',
        'Pediatryczna domowa opieka paliatywna',
        'Pielęgnowanie pacjenta dorosłego wentylowanego mechanicznie',
        'Podstawy opieki paliatywnej',
        'Rehabilitacja osób z przewlekłymi zaburzeniami psychicznymi',
        'Szczepienia ochronne',
        'Wykonanie badania spirometrycznego',
        'Wykonanie konikopunkcji, odbarczenie odmy prężnej oraz wykonanie dojścia doszpikowego',
        'Wykonywanie i ocena testów skórnych',
        'Żywienie dojelitowe i pozajelitowe',
        'Edukator w cukrzycy',
        'Komunikowanie interpersonalne w pielęgniarstwie',
        'Opieka nad osobami z cukrzycą stosującymi terapię ciągłego podskórnego wlewu insuliny CPWI',
        'Opieka pielęgniarska nad chorymi dorosłymi w leczeniu systemowym nowotworów',
        'Ordynowanie leków i wypisywanie recept',
        'Podstawy języka migowego',
        'Resuscytacja krążeniowo-oddechowa',
        'Resuscytacja oddechowo-krążeniowa noworodka',
        'Terapia bólu ostrego u dorosłych',
        'Terapia bólu przewlekłego u dorosłych',
        'Wykonanie i interpretacja zapisu elektrokardiograficznego u dorosłych',
        'Wywiad i badanie fizykalne',
        'Edukacja i wsparcie kobiety w okresie laktacji',
        'Leczenie ran',
        'Monitorowanie dobrostanu płodu w czasie ciąży i podczas porodu',
        'Onkologia ginekologiczna',
        'Opieka nad kobietą z cukrzycą w okresie okołoporodowym',
        'Szczepienia ochronne'
    ]
    courses_raw = [
        {'course_name': specjalizacja, 'education_level': 'specjalizacja'}
        for specjalizacja in specjalizacje
    ] + [
        {'course_name': kurs_kwalifikacyjny, 'education_level': 'kurs kwalifikacyjny'}
        for kurs_kwalifikacyjny in kursy_kwalifikacyjne
    ] + [
        {'course_name': kurs_specjalistyczny, 'education_level': 'kurs specjalistyczny'}
        for kurs_specjalistyczny in kursy_specjalistyczne
    ]

    courses = [
        {
            'id': i, 
            'label': course['course_name'] + ' (' + course['education_level'] + ')',
            'group': course['education_level']
        }
        for i, course in enumerate(courses_raw)
    ]
    education_level = ["specjalizacja", "kurs kwalifikacyjny", "kurs specjalistyczny"]

    return render_template(
        "form.html",
        courses=courses,
        education_level=education_level
    )