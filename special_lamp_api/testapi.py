import sys
sys.path.append('../special_lamp_backend/')

from flask import Flask, jsonify

app = Flask(__name__)

from special_lamp_backend.searchKijiji import getKijijiEntries as skGetKijijiEntries
from special_lamp_backend.searchKijiji import getGPUs as skGetGPUs

@app.route("/getGPUs/", methods=['GET'])
def getGPUs():
    names = skGetGPUs()
    response = jsonify({"gpu_name" : names})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

@app.route("/getKijijiEntries/<gpu_name>", methods=['GET'])
def getKijijiEntries(gpu_name):
    name,price,description = skGetKijijiEntries(gpu_name)
    response = jsonify({"gpu_name" : name, "price" : price, "desc" : description})
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

if __name__ == "__main__":
    app.run(debug=True)