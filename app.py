from flask import Flask, request, jsonify
from flask_pymongo import pymongo
from bson.json_util import dumps
from flask_cors import CORS

app = Flask(__name__)

CORS(app)

client = pymongo.MongoClient("mongodb+srv://nando:nando@dummy.wwzkm7a.mongodb.net/")
db = client["Dummy"]
col_water = db["WaterQuality"]

@app.route('/api/water', methods=['GET'])
def get_all_water():
    waters = col_water.find()
    resp = dumps(waters)
    return resp

# post water
@app.route('/api/water', methods=['POST'])
def add_water():
    _json = request.json
    _ph = _json['ph']
    _tds = _json['tds']
    _temperature = _json['temperature']
    _turbidity = _json['turbidity']
    
    from datetime import datetime
    _date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    if _ph and _tds and _temperature and _turbidity and _date and request.method == 'POST':
        id = col_water.insert_one({
            'ph': _ph,
            'tds': _tds,
            'temperature': _temperature,
            'turbidity': _turbidity,
            'date': _date
        })
        resp = jsonify('Water added successfully')
        resp.status_code = 200
        return resp
    else:
        return not_found()

@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404
    return resp

if __name__ == "__main__":
    app.run(debug=True)