from flask import Flask,jsonify
from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'application/json'

from searchKijiji import getKijijiEntries as skGetKijijiEntries
from searchKijiji import getGPUs as skGetGPUs

@app.route("/getGPUs/", methods=['GET'])
@cross_origin()
def getGPUs():
    names = skGetGPUs()
    return jsonify({"gpu_name" : names})

@app.route("/getKijijiEntries/<gpu_name>", methods=['GET'])
@cross_origin()
def getKijijiEntries(gpu_name):
    name,price,description = skGetKijijiEntries(gpu_name)
    return jsonify({"gpu_name" : name, "price" : price, "desc" : description})

if __name__ == "__main__":
    app.run(debug=True)