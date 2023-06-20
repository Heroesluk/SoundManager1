import os

from flask import send_from_directory, request
from flask import Flask
from flask_cors import CORS

from main import game

app = Flask(__name__, static_folder='static/build')

CORS(app)


@app.route('/', defaults={'path': ''})
@app.route('/<path:path>', methods=['POST', 'GET'])
def serve(path):
    if path != "" and os.path.exists(app.static_folder + '/' + path):
        return send_from_directory(app.static_folder, path)
    else:
        return send_from_directory(app.static_folder, 'index.html')


@app.route("/presentation", methods=['POST', 'GET'])
def resources():

    game(request.json[0]['tips'])
    return "tak"


if __name__ == '__main__':
    app.run()
