from flask import Flask, render_template, jsonify
from flask_executor import Executor
from datetime import datetime
import time
import csv
from .node import global_cpuUsage, global_networkUsage, Node

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG_FILE')
MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']
POOLING_TIME = 10
executor = Executor(app)


# lampnet = [Node(i) for i in range(100)]
# for node in lampnet:
#     node.start()


@app.route('/lampnet_demo')
def lampnet_demo():
    return render_template(
        'lampnet_demo.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY
    )


@app.route('/_update_frame')
def update_frame():
    return jsonify()


@app.route('/_init_lamps')
def init_lamps():
    locations = read_lamp_locations_from_csv()
    return jsonify(locations)


def read_lamp_locations_from_csv():
    with open('points.csv', 'r') as f:
        reader = csv.reader(f)
        return list(reader)
