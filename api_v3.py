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
        print(f"Erreur MySQL : {err}")
        return None

def login():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return False
        
    mydb = get_db_connection()
    if mydb is None:
        return False
        
    cursor = mydb.cursor()
    req = f"SELECT * FROM user WHERE login = '{auth.username}' AND password = '{auth.password}'"
    cursor.execute(req)
    data = cursor.fetchone()
    
    cursor.close()
    mydb.close()
    
    if data:
        return True
    return False

@app.route('/')
def home():
    return 'Page d\'accueil (API v3)'

@app.route('/v3/etudiants/', methods=['GET'])
def getEtudiants():
    if not login():
        return jsonify("Accès refusé"), 401
        
    mydb = get_db_connection()
    if mydb is None:
        return jsonify({"error": "Échec de connexion à la base de données"}), 500
        
    cursor = mydb.cursor()
    req = "SELECT * FROM etudiant"
    cursor.execute(req)
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

@app.route('/v3/etudiants/<int:id>', methods=['GET'])
def getEtudiant(id):
    if not login():
        return jsonify("Accès refusé"), 401
        
    mydb = get_db_connection()
    if mydb is None:
        return jsonify({"error": "Échec de connexion à la base de données"}), 500
        
    cursor = mydb.cursor()
    req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
    
    try:
        cursor.execute(req)
        row = cursor.fetchone()
        etudiant = {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }
        cursor.close()
        mydb.close()
        return jsonify(etudiant), 200
    except TypeError:
        cursor.close()
        mydb.close()
        return jsonify({'erreur': 'id invalide'}), 404

@app.route('/v3/etudiants/', methods=['POST'])
def addEtudiant():
    if not login():
        return jsonify("Accès refusé"), 401
        
    data = request.get_json()
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
    return jsonify({"message": "Ajout OK"}), 201

@app.route('/v3/etudiants/<int:id>', methods=['PUT'])
def updateEtudiant(id):
    if not login():
        return jsonify("Accès refusé"), 401
        
    data = request.get_json()
    nom = data.get('nom')
    prenom = data.get('prenom')
    email = data.get('email')
    telephone = data.get('telephone')
    
    mydb = get_db_connection()
    if mydb is None:
        return jsonify({"error": "Échec de connexion à la base de données"}), 500
        
    cursor = mydb.cursor()
    query = f"UPDATE etudiant SET nom = '{nom}', prenom = '{prenom}', email = '{email}', telephone = '{telephone}' WHERE idetudiant = {id}"
    cursor.execute(query)
    mydb.commit()
    
    affected_rows = cursor.rowcount
    cursor.close()
    mydb.close()
    
    if affected_rows == 0:
        return jsonify({'erreur': 'id invalide'}), 404
        
    return jsonify({"message": "Modification OK"}), 200


@app.route('/v3/etudiants/<int:id>', methods=['DELETE'])
def deleteEtudiant(id):
    if not login():
        return jsonify("Accès refusé"), 401
        
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
        return jsonify({'erreur': 'id invalide'}), 404
        
    return jsonify({"message": "Suppression OK"}), 200

if __name__ == '__main__':
    app.run(debug=True)
