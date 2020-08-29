from flask import Flask, render_template
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

def prepare_regions(file_path):
    with open(file_path, encoding='utf8') as f:
        regions = json.load(f)["features"]
    for region in regions:
        center_x = 0
        center_y = 0
        counter = 0
        if region['geometry']['type'] == "Polygon":
            coordinates = region['geometry']['coordinates'][0]
        else:
            coordinates = []
            for coordinate_list in region['geometry']['coordinates'][0]:
                coordinates.extend(coordinate_list)

        for coordinate in coordinates:
            center_x += coordinate[0]
            center_y += coordinate[1]
            counter += 1
        center_x = center_x / counter
        center_y = center_y / counter
        region["center"] = [center_x, center_y]
    return regions


@app.route('/')
def index():
    wojewodztwa = prepare_regions("static/maps/wojewodztwa-min.geojson")
    powiaty = prepare_regions("static/maps/powiaty-min.geojson")
    
    return render_template("index.html", wojewodztwa=wojewodztwa, powiaty=powiaty)