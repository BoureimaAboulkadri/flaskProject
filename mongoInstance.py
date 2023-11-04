from flask import Flask, jsonify, request
from pymongo import MongoClient

app = Flask(__name__)
app.env = "development"

# Établir une connexion avec MongoDB
client = MongoClient("mongodb+srv://diallokader9:IBF48nGiqdSmT0tq@carpredict.mkqgumi.mongodb.net/?retryWrites=true&w=majority")
db = client.mydatabase
collection = db.mycollection

# Route pour récupérer toutes les données
@app.route('/data', methods=['GET'])
def get_all_data():
    data = list(collection.find())
    for item in data:
        item["_id"] = str(item["_id"])  # Convertir ObjectID en string pour le rendre JSON serializable
    return jsonify(data)

# Route pour ajouter de nouvelles données
@app.route('/data', methods=['POST'])
def add_data():
    data = request.json
    collection.insert_one(data)
    return jsonify({"message": "Data added successfully!"})

# (Vous pouvez ajouter d'autres routes pour les opérations de mise à jour et de suppression si nécessaire)

if __name__ == '__main__':
    app.run(debug=True)
