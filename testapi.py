from flask import Flask,jsonify
app = Flask(__name__)

from searchKijiji import getKijijiEntries as skGetKijijiEntries
from searchKijiji import getGPUs as skGetGPUs

@app.route("/getGPUs/", methods=['GET'])
def getGPUs():
    names = skGetGPUs()
    return jsonify({"gpu_name" : names})

@app.route("/getKijijiEntries/<gpu_name>", methods=['GET'])
def getKijijiEntries(gpu_name):
    name,price,description = skGetKijijiEntries(gpu_name)
    return jsonify({"gpu_name" : name, "price" : price, "desc" : description})

if __name__ == "__main__":
    app.run(debug=True)