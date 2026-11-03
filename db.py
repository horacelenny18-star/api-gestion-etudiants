import mysql.connector

class Database:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            return self.connection
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")
            return None

    def authorized(self, username, password):
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        req = f"SELECT * FROM user WHERE login = '{username}' AND password = '{password}'"
        cursor.execute(req)
        data = cursor.fetchone()
        cursor.close()
        conn.close()
        return data is not None

    def readAll(self):
        conn = self.connect()
        if not conn:
            return None
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM etudiant")
        result = cursor.fetchall()
        
        etudiants = []
        for row in result:
            etudiants.append({
                "idetudiant": row[0],
                "nom": row[1],
                "prenom": row[2],
                "email": row[3],
                "telephone": row[4]
            })
        cursor.close()
        conn.close()
        return etudiants

    def readOne(self, id):
        conn = self.connect()
        if not conn:
            return None
        cursor = conn.cursor()
        req = f"SELECT * FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(req)
        row = cursor.fetchone()
        cursor.close()
        conn.close()
        
        if row is None:
            return None
            
        return {
            "idetudiant": row[0],
            "nom": row[1],
            "prenom": row[2],
            "email": row[3],
            "telephone": row[4]
        }

    def create(self, nom, prenom, email, telephone):
        conn = self.connect()
        if not conn:
            return False
        cursor = conn.cursor()
        query = f"INSERT INTO etudiant (nom, prenom, email, telephone) VALUES ('{nom}', '{prenom}', '{email}', '{telephone}')"
        cursor.execute(query)
        conn.commit()
        cursor.close()
        conn.close()
        return True

    def update(self, id, nom, prenom, email, telephone):
        conn = self.connect()
        if not conn:
            return 0
        cursor = conn.cursor()
        query = f"UPDATE etudiant SET nom = '{nom}', prenom = '{prenom}', email = '{email}', telephone = '{telephone}' WHERE idetudiant = {id}"
        cursor.execute(query)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected

    def delete(self, id):
        conn = self.connect()
        if not conn:
            return 0
        cursor = conn.cursor()
        query = f"DELETE FROM etudiant WHERE idetudiant = {id}"
        cursor.execute(query)
        conn.commit()
        affected = cursor.rowcount
        cursor.close()
        conn.close()
        return affected
