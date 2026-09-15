import mysql.connector

class Database:
    def __init__(self):
        self.host = "127.0.0.1"
        self.user = "extern_user"
        self.password = "bt5@c13l972"
        self.database = "ciel2027"

    def connect(self):
        try:
            return mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except mysql.connector.Error as err:
            print(f"Erreur MySQL : {err}")
            return None

    def readAll(self):
        db = self.connect()
        if db is None:
            return None
        cursor = db.cursor()
        cursor.execute("SELECT * FROM etudiant")
        result = cursor.fetchall()
        cursor.close()
        db.close()
        return result

    def readOne(self, id_etudiant):
        db = self.connect()
        if db is None:
            return None
        cursor = db.cursor()
        query = f"SELECT * FROM etudiant WHERE idetudiant = {id_etudiant}"
        cursor.execute(query)
        row = cursor.fetchone()
        cursor.close()
        db.close()
        return row

    def create(self, nom, prenom, email, telephone):
        db = self.connect()
        if db is None:
            return False
        cursor = db.cursor()
        query = "INSERT INTO etudiant (nom, prenom, email, telephone) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (nom, prenom, email, telephone))
        db.commit()
        cursor.close()
        db.close()
        return True

    def update(self, id_etudiant, nom, prenom, email, telephone):
        db = self.connect()
        if db is None:
            return 0
        cursor = db.cursor()
        query = "UPDATE etudiant SET nom = %s, prenom = %s, email = %s, telephone = %s WHERE idetudiant = %s"
        cursor.execute(query, (nom, prenom, email, telephone, id_etudiant))
        db.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        db.close()
        return affected_rows

    def delete(self, id_etudiant):
        db = self.connect()
        if db is None:
            return 0
        cursor = db.cursor()
        query = f"DELETE FROM etudiant WHERE idetudiant = {id_etudiant}"
        cursor.execute(query)
        db.commit()
        affected_rows = cursor.rowcount
        cursor.close()
        db.close()
        return affected_rows

    def login(self, login_user, password_user):
        db = self.connect()
        if db is None:
            return None
        cursor = db.cursor()
        query = "SELECT * FROM user WHERE login = %s AND password = %s"
        cursor.execute(query, (login_user, password_user))
        row = cursor.fetchone()
        cursor.close()
        db.close()
        return row