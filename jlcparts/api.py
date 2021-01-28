import json

from flask import Flask
from flask_restful import Resource, Api
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

from config import CSV_FILE, JSON_FILE
from datatables import buildtables
from ui import getLibrary

app = Flask(__name__)
api = Api(app)


class Handler(FileSystemEventHandler):
    def on_modified(self, event):
        if CSV_FILE == event.src_path:
            print("File Changed, rebuilding database")
            try:
                getLibrary(CSV_FILE, JSON_FILE)
                buildtables(JSON_FILE, 'data')
            except:
                print("something went wrong")


class FetchJSON(Resource):
    def get(self, filename):
        with open(f'data/{filename}') as index:
            string = index.read()
            idx = json.loads(string)
        return idx, 200, {'Access-Control-Allow-Origin': '*'}


class FetchText(Resource):
    def get(self, filename):
        with open(f'data/{filename}') as index:
            string = index.read()
        return string, 200, {'Access-Control-Allow-Origin': '*'}


api.add_resource(FetchJSON, '/json/<string:filename>')
api.add_resource(FetchText, '/text/<string:filename>')

observer = Observer()
observer.schedule(Handler(), "..")  # watch the local directory
observer.start()

if __name__ == '__main__':
    getLibrary(CSV_FILE, JSON_FILE)
    buildtables(JSON_FILE, 'data')
    app.run(debug=True)
