from flask import Flask, Response, render_template
from config import neo_credentials, debug
from model import GraphManager
import json

graph = GraphManager(neo_credentials, "6Q3Gzq", "187170","4FBF01FF-390C-46AB-A3CF-D0827CAD86B9","Team4")

app = Flask(__name__)

@app.route('/')
def json_home():
    jresponse = {"msj": "Hello World!"}
    r = Response(json.dumps(jresponse), status=200, mimetype="application/json")
    return r


@app.route('/test_template')
def test_template():
    cities = graph.get_cities()
    return render_template('template.html', cities=cities)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=debug)