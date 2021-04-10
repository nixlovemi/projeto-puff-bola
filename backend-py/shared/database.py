import mysql.connector as db

def getConnection():
    mydb = db.connect(
        host="projeto-puff-bola_db_1",
        user="admin",
        password="password",
        database="db"
    )
    mydb.autocommit = True
    return mydb
