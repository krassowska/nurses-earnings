import csv
import json


def test_has_uppercase(region):
    return not region["properties"]["nazwa"].islower()


def test_is_lowercase(region):
    return region["properties"]["nazwa"].islower()


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