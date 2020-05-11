from flask import Flask, request, session, g, redirect, \
    url_for, abort, render_template, flash

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG_FILE')

MAPBOX_ACCESS_KEY = app.config['MAPBOX_ACCESS_KEY']


@app.route('/lampnet_demo')
def mapbox_js():
    return render_template(
        'lampnet_demo.html',
        ACCESS_KEY=MAPBOX_ACCESS_KEY
    )

