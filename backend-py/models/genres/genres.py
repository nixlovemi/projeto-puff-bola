from shared.database import getConnection
import mysql.connector
import sys


def getGenres(genre_id=None):
    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = " SELECT id, name, active "
    sql += " FROM genres "
    sql += " WHERE active = 1 "

    if genre_id is not None:
        if genre_id.isnumeric() and int(genre_id) > 0:
            sql += " AND id = " + genre_id

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    arrGenre = []
    for x in myresult:
        dictGenre = {}
        dictGenre['id'] = x[0]
        dictGenre['name'] = x[1]
        dictGenre['actve'] = x[2]

        arrGenre.append(dictGenre)

    return arrGenre


def insertGenres(genre):
    error = False
    msg = 'Gênero cadastrado com sucesso!!!'

    if genre is None or genre.split() == "" or len(genre) > 30:
        error = True
        msg = 'Erro! Gênero Inválido! Tente uma opção válida!'
    else:
        mydb = getConnection()
        mycursor = mydb.cursor()
        sql = f'SELECT id FROM genres WHERE name = "{genre}" AND active = 1'
        mycursor.execute(sql)
        myresult = mycursor.fetchall()
        if len(myresult) > 0:
            error = True
            msg = 'Erro! Gênero já cadastrado!'
        else:
            sqlInsert = (f"INSERT INTO genres (name) VALUES ( '{genre}')")
            mycursor.execute(sqlInsert)
            if mycursor.rowcount <= 0:
                error = True
                msg = 'Erro ao adicionar o gênero'

    objReturn = {}
    objReturn['error'] = error
    objReturn['msg'] = msg
    return objReturn


def updateGenres(genre):
    genre_id = genre['genre_id']
    genre = genre['name'].strip()
    error = False
    msg = 'Gênero alterado com Sucesso!'
    objReturn = {}

    if genre_id is None or not genre_id.isnumeric or int(genre_id) <= 0 or genre is None or genre == "" or len(genre) > 30:
        error = True
        msg = 'Erro! Gênero inválido!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn

    else:
        mydb = getConnection()
        mycursor = mydb.cursor()

        try:
            sqlUpdate = f'UPDATE genres SET name = "{genre}" WHERE id = {genre_id} AND active = 1;'
            mycursor.execute(sqlUpdate)

            if mycursor.rowcount <= 0:
                msg = 'Alerta! Gênero inativo!'

        except mysql.connector.Error as err:
            error = True
            msg = f'Erro: {err.msg} na linha: {sys.exc_info()[-1].tb_lineno}'

    objReturn['msg'] = msg
    objReturn['error'] = error
    return objReturn


def deleteGenres(genre_id):
    error = False
    msg = 'Genero deletado com Sucesso!'

    if genre_id is None:
        genre_id = 0

    if genre_id.isnumeric and int(genre_id) > 0:
        # "deleta" o genero mudando de ativo para inativo no banco
        mydb = getConnection()
        mycursor = mydb.cursor()

        try:
            sqlDelete = f'UPDATE genres SET active = 0 WHERE id = {genre_id};'
            mycursor.execute(sqlDelete)

        except mysql.connector.Error as err:
            error = True
            msg = f'Erro: {err.msg} na linha: {sys.exc_info()[-1].tb_lineno}'

    else:
        error = True
        msg = 'Erro! Gênero inválido, tente novamente!'

    objReturn = {}
    objReturn['msg'] = msg
    objReturn['error'] = error
    return objReturn
