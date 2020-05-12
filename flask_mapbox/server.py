from flask import Flask, render_template, jsonify
import json
import csv
from .node import global_cpuUsage, Node

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG_FILE')
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']
POOLING_TIME = 10

lampnet = [Node(i) for i in range(100)]
for node in lampnet:
    node.start()


@app.route('/lampnet_demo')
def lampnet_demo():
    return render_template(
        'lampnet_demo.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY
    )


@app.route('/_update_frame')
def update_frame():
    with open('static/map.geojson', 'r') as f:
        data = json.load(f)
        for features in data["features"]:
            features["properties"]["task_type"] = global_cpuUsage[features["properties"]["id"]][1]
    return jsonify(data)


@app.route('/_init_lamps')
def init_lamps():
    locations = read_lamp_locations_from_csv()
    return jsonify(locations)


@app.route('/_init_lamps_json')
def init_lamps_json():
    with open('static/map.geojson', 'r') as f:
        data = json.load(f)
        for features in data["features"]:
            features["properties"]["task_type"] = 0
    return jsonify(data)


def read_lamp_locations_from_csv():
    with open('points.csv', 'r') as f:
        reader = csv.reader(f)
        return list(reader)
