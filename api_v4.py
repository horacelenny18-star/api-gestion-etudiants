from flask import Flask, jsonify, request
from db import Database

app = Flask(__name__)


db = Database(host="127.0.0.1", user="extern_user", password="bt5@c13l972", database="ciel2027")

def check_auth():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return False
    return db.authorized(auth.username, auth.password)

@app.route('/')
def home():
    return 'Page d\'accueil (API v4 - POO)'

@app.route('/v4/etudiants/', methods=['GET'])
def getEtudiants():
    if not check_auth():
        return jsonify("Accès refusé"), 401
    
    result = db.readAll()
    if result is None:
        return jsonify({"error": "Échec de connexion à la base de données"}), 500
        
    return jsonify(result), 200

@app.route('/v4/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    if not check_auth():
        return jsonify("Accès refusé"), 401
        
    try:
        etudiant = db.readOne(id)
        if etudiant is None:
            return jsonify({'erreur': 'id invalide'}), 404
        return jsonify(etudiant), 200
    except Exception:
        return jsonify({'erreur': 'id invalide'}), 404

@app.route('/v4/etudiants/', methods=['POST'])
def addEtudiant():
    if not check_auth():
        return jsonify("Accès refusé"), 401
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données JSON manquantes"}), 400
        
    success = db.create(data.get('nom'), data.get('prenom'), data.get('email'), data.get('telephone'))
    if not success:
        return jsonify({"error": "Échec de connexion à la base de données"}), 500
        
    return jsonify({"message": "Ajout OK"}), 201

@app.route('/v4/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if not check_auth():
        return jsonify("Accès refusé"), 401
        
    data = request.get_json()
    if not data:
        return jsonify({"error": "Données JSON manquantes"}), 400
        
    affected = db.update(id, data.get('nom'), data.get('prenom'), data.get('email'), data.get('telephone'))
    if affected == 0:
        return jsonify({'erreur': 'id invalide'}), 404
        
    return jsonify({"message": "Modification OK"}), 200

@app.route('/v4/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    if not check_auth():
        return jsonify("Accès refusé"), 401
        
    affected = db.delete(id)
    if affected == 0:
        return jsonify({'erreur': 'id invalide'}), 404
        
    return jsonify({"message": "Suppression OK"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
