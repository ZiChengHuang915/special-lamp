from flask import Flask,jsonify
app = Flask(__name__)

from searchKijiji import getKijijiEntries

@app.route("/kijijiDeal/<gpu_name>", methods=['GET'])
def kijijiDeal(gpu_name):
  name,price,description = getKijijiEntries(gpu_name)
  return jsonify({"gpu_name" : name, "price" : price, "desc" : description})

if __name__ == "__main__":
    app.run(debug=True)