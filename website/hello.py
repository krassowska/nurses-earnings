from flask import Flask, render_template
import json

app = Flask(__name__)
app.config['TEMPLATES_AUTO_RELOAD'] = True

@app.route('/')
def index():
    with open("static/maps/wojewodztwa-min.geojson", encoding='utf8') as f:
        wojewodztwa = json.load(f)["features"]
    for wojewodztwo in wojewodztwa:
        #center = wojewodztwo['geometry']['coordinates'][0][0]
        center_x = 0
        center_y = 0
        counter = 0
        for coodinate in wojewodztwo['geometry']['coordinates'][0]:
            center_x += coodinate[0]
            center_y += coodinate[1]
            counter += 1
        center_x = center_x / counter
        center_y = center_y / counter
        print(center_x, center_y)
        wojewodztwo["center"] = [center_x, center_y]
        print(wojewodztwo["center"])
    return render_template("index.html", wojewodztwa=wojewodztwa)