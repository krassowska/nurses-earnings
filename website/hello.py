from flask import Flask, render_template
import json
import csv

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True


def test_has_uppercase(region):
    return not region["properties"]["nazwa"].islower()


def test_is_lowercase(region):
    return region["properties"]["nazwa"].islower()


app.jinja_env.tests['has_uppercase'] = test_has_uppercase
app.jinja_env.tests['is_lowercase'] = test_is_lowercase


def prepare_regions(file_path):
    with open(file_path, encoding='utf8') as f:
        regions = json.load(f)["features"]

    for region in regions:
        center_x = 0
        center_y = 0
        counter = 0

        h_to_w_ratio = 10.7 / 6.5

        if region['geometry']['type'] == "Polygon":
            coordinates = region['geometry']['coordinates'][0]
        else:
            coordinates = []
            for coordinate_list in region['geometry']['coordinates'][0]:
                coordinates.extend(coordinate_list)

        west_border = 999
        north_border = -999
        east_border = -999
        south_border = 999

        for coordinate in coordinates:
            coordinate[1] = coordinate[1] * h_to_w_ratio
            center_x += coordinate[0]
            center_y += coordinate[1]
            counter += 1
            if coordinate[0] < west_border:
                west_border = coordinate[0]
            
            if coordinate[1] > north_border:
                north_border = coordinate[1]
                
            if coordinate[0] > east_border:
                east_border = coordinate[0]
            
            if coordinate[1] < south_border:
                south_border = coordinate[1]
            
        center_x = center_x / counter
        center_y = center_y / counter
        width = east_border - west_border
        height = north_border - south_border
        region["center"] = [center_x, center_y]
        
        region["west_border"] = west_border
        region["north_border"] = north_border
        region["east_border"] = east_border
        region["south_border"] = south_border
        region["width"] = width
        region["height"] = height
    return regions

def prepare_powiats_data(file_path):
    with open(file_path, newline='', encoding='utf-8') as csvfile:
        powiats_data = csv.DictReader(csvfile)
        powiaty = {}
        for row in powiats_data:
            key = row['\ufeffPowiat']
            powiaty[key] = row
            # print(row)
        print(powiaty)
    return powiaty



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
        {'id': i, 'label': course['course_name'] + ' (' + course['education_level'] + ')'}
        for i, course in enumerate(courses_raw)
    ]
    
    return render_template(
        "form.html",
        courses=courses
    )