from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

db = {"C25725": {
    "lcsc": "C25725",
    "category": "Resistors",
    "subcategory": "Resistor Networks & Arrays",
    "mfr": "4D02WGJ0103TCE",
    "package": "0402_x4",
    "joints": 8,
    "manufacturer": "Uniroyal Elec",
    "basic": True,
    "description": "Resistor Networks & Arrays 10KOhms \u00b15% 1/16W 0402_x4 RoHS",
    "datasheet": "https://datasheet.lcsc.com/szlcsc/Uniroyal-Elec-4D02WGJ0103TCE_C25725.pdf",
    "stock": 67586,
    "price": [
        {
            "qFrom": 1,
            "qTo": 199,
            "price": 0.005210145
        },
        {
            "qFrom": 200,
            "qTo": None,
            "price": 0.001866667
        }
    ], }
}


class PartsStock(Resource):
    def get(self, partName):
        return db.get(partName, None)

api.add_resource(PartsStock, '/<string:partName>')

if __name__ == '__main__':
    app.run(debug=True)
