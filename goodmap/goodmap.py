from flask import Flask
from flask import render_template, request, current_app
import os
import json
from flask import jsonify


def load_json(file):
    with open(file, 'r') as file:
        return json.load(file)


def does_fulfill_requriement(entry, requirements):
    matches = []
    for category, values in requirements:
        if not values:
            continue
        matches.append(all(entry_value in entry[category] for entry_value in values))
    return all(matches)


def create_app():
    app = Flask(__name__)
    DATA = os.getenv('DATA')
    app.config['data'] = load_json(DATA)

    @app.context_processor
    def setup_context():
        return dict(app_name=app.config['data']['app_name'])

    @app.route("/")
    def index():
        return render_template('map.html')

    @app.route("/data")
    def get_data():
        local_data = app.config["data"]["data"]
        query_params = request.args.to_dict(flat=False)
        categories = app.config["data"]["categories"]
        requirements = []
        for key in categories.keys():
            requirements.append((key, query_params.get(key)))

        filtered_data = filter(lambda x: does_fulfill_requriement(x, requirements), local_data)
        return jsonify(list(filtered_data))

    @app.route("/api/categories")
    def get_categories():
        data = list(app.config["data"]["categories"].keys())
        return jsonify(data)

    @app.route("/api/category/<category_type>")
    def get_category_types(category_type):
        local_data = app.config["data"]["categories"][category_type]
        return jsonify(local_data)

    return app
