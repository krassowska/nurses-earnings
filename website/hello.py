from flask import Flask, render_template
import json

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
    
    return render_template(
        "index.html",
        wojewodztwa=wojewodztwa,
        powiaty=powiaty,
        poland_west_most=poland_west_most,
        poland_north_most=poland_north_most,
        poland_width=poland_width,
        poland_height=poland_height
    )