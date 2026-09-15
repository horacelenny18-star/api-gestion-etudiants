from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

def get_db_connection():
    try:
        return mysql.connector.connect(
            host="127.0.0.1",
            user="extern_user",
            password="bt5@c13l972",
            database="ciel2027"
        )
    except mysql.connector.Error as err:
        print(f"Erreur de connexion MySQL : {err}")
        return None

@app.route('/')
def home():
    return 'Page d\'accueil (API v2)'

@app.route('/v2/etudiants/', methods=['GET'])
def getEtudiants():
    try:
        mydb = get_db_connection()
        if mydb is None:
            return jsonify({"error": "Échec de connexion à la base de données"}), 500
            
        cursor = mydb.cursor()
        query = "SELECT * FROM etudiant"
        cursor.execute(query)
        result = cursor.fetchall()
        
        etudiants = []
        for row in result:
            etudiant = {
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            }
            etudiants.append(etudiant)
            
        cursor.close()
        mydb.close()
        return jsonify(etudiants), 200
    except Exception as e:
        return jsonify({"error": "Erreur interne du serveur"}), 500

@app.route('/v2/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    mydb = get_db_connection()
    if mydb is None:
        return jsonify({"error": "Échec de connexion à la base de données"}), 500
        
    cursor = mydb.cursor()
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    print(req)
    try:
        cursor.execute(req)
        row = cursor.fetchone()
        
        cursor.close()
        mydb.close()
        
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        return jsonify(etudiant), 200
    except TypeError:
        cursor.close()
        mydb.close()
        return jsonify({'erreur': 'id invalide'}), 404

@app.route('/v2/etudiants/', methods=['POST'])
def addEtudiant():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "Données JSON manquantes"}), 400
            
        nom = data.get('nom')
        prenom = data.get('prenom')
        email = data.get('email')
        telephone = data.get('telephone')
        
        mydb = get_db_connection()
        if mydb is None:
            return jsonify({"error": "Échec de connexion à la base de données"}), 500
            
        cursor = mydb.cursor()
        query = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES ('{nom}', '{prenom}', '{email}', '{telephone}')"
        cursor.execute(query)
        mydb.commit()
        
        cursor.close()
        mydb.close()
        return jsonify({"message": "Étudiant ajouté avec succès"}), 201
    except Exception as e:
        return jsonify({"error": "Erreur lors de l'insertion des données"}), 500

@app.route('/v2/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    try:
        mydb = get_db_connection()
        if mydb is None:
            return jsonify({"error": "Échec de connexion à la base de données"}), 500
            
        cursor = mydb.cursor()
        query = f"DELETE FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(query)
        mydb.commit()
        
        affected_rows = cursor.rowcount
        cursor.close()
        mydb.close()
        
        if affected_rows == 0:
            return jsonify({"error": "Étudiant non trouvé"}), 404
            
        return jsonify({"message": "Étudiant supprimé avec succès"}), 200
    except Exception as e:
        return jsonify({"error": "Impossible de supprimer l'étudiant"}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)