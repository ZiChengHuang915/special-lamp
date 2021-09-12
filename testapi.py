from flask import Flask,jsonify
app = Flask(__name__)

from searchKijiji import getKijijiEntries

@app.route("/getGPUs/", methods=['GET'])
def getGPUs():
    names = getGPUs()
    return jsonify({"gpu_name" : names})

@app.route("/getKijijiDeal/<gpu_name>", methods=['GET'])
def getKijijiDeal(gpu_name):
    name,price,description = getKijijiEntries(gpu_name)
    return jsonify({"gpu_name" : name, "price" : price, "desc" : description})

if __name__ == "__main__":
    app.run(debug=True)