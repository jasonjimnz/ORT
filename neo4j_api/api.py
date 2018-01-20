from flask import Flask, Response
from config import neo_credentials, debug
from model import GraphManager
import json

graph = GraphManager(neo_credentials)

app = Flask(__name__)

@app.route('/')
def json_home():
    jresponse = {"msj": "Hello World!"}
    r = Response(json.dumps(jresponse), status=200, mimetype="application/json")
    return r

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=3000, debug=debug)