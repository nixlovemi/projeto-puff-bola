from shared.database import getConnection
from datetime import datetime
import mysql.connector
import sys

presentYear = datetime.today().year


def getMovies(movie_id=None):
    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = " SELECT id, title, isan, trailer_url, duration, release_year, active "
    sql += " FROM movies "
    sql += " WHERE active = 1 "

    if movie_id is not None:
        if movie_id.isnumeric() and int(movie_id) > 0:
            sql += " AND id = " + movie_id

    mycursor.execute(sql)
    myresult = mycursor.fetchall()

    arrMovies = []
    for x in myresult:
        dictMovies = {}
        dictMovies['id'] = x[0]
        dictMovies['title'] = x[1]
        dictMovies['isan'] = x[2]
        dictMovies['trailer_url'] = x[3]
        dictMovies['duration'] = x[4]
        dictMovies['release_year'] = x[5]
        dictMovies['active'] = x[6]

        arrMovies.append(dictMovies)

    return arrMovies


def insertMovies(movie):
    import json

    title = movie['title'].strip()
    genre_id = movie['genre_id']
    isan = movie['isan'].strip()
    trailerUrl = movie['trailerUrl'].strip()
    rating = movie['rating']
    releaseYear = movie['releaseYear']
    duration = movie['duration']
    msg = 'Filme Cadastrado com sucesso!'
    error = False
    objReturn = {}

    # Tratamento das Variaveis
    if title is None:
        title = ''
    try:
        arrGenre = json.loads(genre_id)
    except:
        arrGenre = None
    if duration is None or not duration.isnumeric():
        duration = -1
    else:
        duration = int(duration)
    if trailerUrl == '':
        trailerUrl = 'Null'
    else:
        trailerUrl = "'" + trailerUrl + "'"
    if rating is None or not rating.isnumeric():
        rating = -1
    else:
        rating = int(rating)
    if releaseYear is None or not releaseYear.isnumeric():
        releaseYear = -1
    else:
        releaseYear = int(releaseYear)
    if isan is None:
        isan = ''

    # Validação das Variaveis
    mydb = getConnection()
    mycursor = mydb.cursor()

    if len(title) > 100 or title == '':
        error = True
        msg = 'Erro! Título Inválido, Insira Título com até 100 caracteres!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn

    if arrGenre is None:
        error = True
        msg = 'Erro! Favor escolher um Gênero válido'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    else:
        valores = ""

        for x in arrGenre:
            valores += f'{str(arrGenre[x])}, '

        valores += "-1"

        sql = f'SELECT COUNT(*) FROM genres WHERE id IN ({valores}) AND active = 1'
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        count = myresult[0]

        if len(arrGenre) != count:
            error = True
            msg = 'Erro! Um ou mais  generos inexistentes!'

            objReturn['msg'] = msg
            objReturn['error'] = error
            return objReturn

    if duration < 0 or duration > 999:
        error = True
        msg = 'Erro! Duração Inválida!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    if releaseYear < 1895 or releaseYear > presentYear:
        error = True
        msg = 'Erro! Ano de lançamento inválido!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    if rating > 10 or rating < 0:
        error = True
        msg = 'Erro! Favor escolher uma nota entre 0 e 10!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn

    # valida se o ISAN ja foi usado e se é valido
    retIsan = validarISAN(isan)
    if retIsan['error']:
        error = True
        msg = retIsan['msg']

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    else:
        # Inserindo Filme na tabela
        if not error:
            sqlInsert = (f"INSERT INTO movies (title, isan, trailer_url, duration, release_year) "
                         f"VALUES ( '{title}', '{isan}', {trailerUrl}, {duration}, {releaseYear})")
            try:
                mycursor.execute(sqlInsert)
            except mysql.connector.Error as err:
                error = True
                msg = f'Erro: {err.msg} na linha: {sys.exc_info()[-1].tb_lineno}'

                objReturn['msg'] = msg
                objReturn['error'] = error
                return objReturn

            if mycursor.rowcount <= 0:
                error = True
                msg = 'Erro ao adicionar o Filme'

                objReturn['msg'] = msg
                objReturn['error'] = error
                return objReturn
            else:
                # faz o vinculo do filme com o genero na tabela movies_genres
                movieLastId = mycursor.lastrowid

                try:
                    for x in arrGenre:
                        sqlInsertGenre = f"INSERT INTO movies_genres (genre_id, movie_id) VALUES ({arrGenre[x]}, {movieLastId})"
                        mycursor.execute(sqlInsertGenre)

                except mysql.connector.Error as err:
                    error = True
                    msg = f'Erro: {err.msg} na linha: {sys.exc_info()[-1].tb_lineno}'

                    objReturn['msg'] = msg
                    objReturn['error'] = error
                    return objReturn

                if mycursor.rowcount <= 0:
                    error = True
                    msg = 'Erro ao vincular o Genero!'

                    objReturn['msg'] = msg
                    objReturn['error'] = error
                    return objReturn

                # faz o vinculo do filme com a nota na tabela movies_rating
                sqlInsertRating = f'INSERT INTO movies_rating (movie_id, rating) VALUES ({movieLastId}, {rating})'
                try:
                    mycursor.execute(sqlInsertRating)
                except mysql.connector.Error as err:
                    error = True
                    msg = f'Erro: {err.msg} na linha: {sys.exc_info()[-1].tb_lineno}'

                    objReturn['msg'] = msg
                    objReturn['error'] = error
                    return objReturn

                if mycursor.rowcount <= 0:
                    error = True
                    msg = 'Erro ao vincular a Nota!'

                    objReturn['msg'] = msg
                    objReturn['error'] = error
                    return objReturn

    objReturn['msg'] = msg
    objReturn['error'] = error
    return objReturn


def validarISAN(isan, movie_id=None):
    import re

    x = re.search("^[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}", isan)

    if x:
        error = False
        msg = 'ISAN válido!'
    else:
        error = True
        msg = 'Erro! ISAN inválido!'

    mydb = getConnection()
    mycursor = mydb.cursor()

    sql = f' SELECT id FROM movies WHERE isan = "{isan}" '
    mycursor.execute(sql)
    myresult = mycursor.fetchone()

    if myresult is not None and int(movie_id) != myresult[0]:
            error = True
            msg = 'Erro! ISAN já cadastrado em outro filme!'

    objReturn = {}
    objReturn['msg'] = msg
    objReturn['error'] = error
    return objReturn


def updateMovie(movie):
    import json

    movie_id = movie['movie_id']
    title = movie['title'].strip()
    genre_id = movie['genre_id']
    isan = movie['isan'].strip()
    trailerUrl = movie['trailerUrl'].strip()
    duration = movie['duration']
    releaseYear = movie['releaseYear']
    error = False
    msg = 'Filme alterado com sucesso!'
    objReturn = {}

    # tratamento das variaveis
    if title is None:
        title = ''
    try:
        arrGenre = json.loads(genre_id)
    except:
        arrGenre = None
    if isan is None:
        isan = ''
    if trailerUrl == '':
        trailerUrl = 'Null'
    else:
        trailerUrl = "'" + trailerUrl + "'"
    if duration is None or not duration.isnumeric():
        duration = -1
    else:
        duration = int(duration)
    if releaseYear is None or not releaseYear.isnumeric():
        releaseYear = -1
    else:
        releaseYear = int(releaseYear)

    # Validação das Variaveis
    mydb = getConnection()
    mycursor = mydb.cursor()

    if len(title) > 100 or title == '':
        error = True
        msg = 'Erro! Título Inválido, Insira Título com até 100 caracteres!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn

    if arrGenre is None:
        error = True
        msg = 'Erro! Favor escolher um Gênero válido'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    else:
        valores = ""

        for x in arrGenre:
            valores += f'{str(arrGenre[x])}, '

        valores += "-1"

        sql = f'SELECT COUNT(*) FROM genres WHERE id IN ({valores}) AND active = 1'
        mycursor.execute(sql)
        myresult = mycursor.fetchone()
        count = myresult[0]

        if len(arrGenre) != count:
            error = True
            msg = 'Erro! Um ou mais  generos inexistentes!'

            objReturn['msg'] = msg
            objReturn['error'] = error
            return objReturn

    if duration < 0 or duration > 999:
        error = True
        msg = 'Erro! Duração Inválida!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    if releaseYear < 1895 or releaseYear > presentYear:
        error = True
        msg = 'Erro! Ano de lançamento inválido!'

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn

    # valida se o ISAN ja foi usado e se é valido
    retIsan = validarISAN(isan, movie_id)

    if retIsan['error']:
        error = True
        msg = retIsan['msg']

        objReturn['msg'] = msg
        objReturn['error'] = error
        return objReturn
    else:
        # editar Filme na tabela
        if not error:
            sqlEdit = (f"UPDATE movies SET title = '{title}', isan = '{isan}', trailer_url = {trailerUrl}, duration = {duration}, "
                       f"release_year = {releaseYear} WHERE id = {movie_id} AND active = 1;")
            try:
                mycursor.execute(sqlEdit)
            except Exception as e:
                error = True
                msg = f'Erro: {e!r} na linha: {sys.exc_info()[-1].tb_lineno}'

                objReturn['msg'] = msg
                objReturn['error'] = error
                return objReturn

            # edita o vinculo do filme com o genero na tabela movies_genres
            try:
                sqlEditGenre = f"DELETE FROM movies_genres WHERE movie_id = {movie_id};"
                mycursor.execute(sqlEditGenre)

                for x in arrGenre:
                    sqlEditGenre = f"INSERT INTO movies_genres (movie_id, genre_id) VALUES ({movie_id}, {arrGenre[x]});"
                    mycursor.execute(sqlEditGenre)

            except mysql.connector.Error as err:
                error = True
                msg = f'Erro: {err.msg} na linha: {sys.exc_info()[-1].tb_lineno}'

    objReturn['msg'] = msg
    objReturn['error'] = error
    return objReturn


def deleteMovie(movie_id):
    error = False
    msg = 'Filme deletado com sucesso!'

    if movie_id is None:
        movie_id = 0

    if movie_id.isnumeric and int(movie_id) > 0:
        # "deleta" o filme mudando de ativo para inativo no banco
        mydb = getConnection()
        mycursor = mydb.cursor()
        sqlUpdate = f'UPDATE movies SET active = 0 WHERE id = {movie_id}'
        mycursor.execute(sqlUpdate)
        if mycursor.rowcount <= 0:
            error = True
            msg = 'Erro! Não foi possivel deletar o filme'
    else:
        error = True
        msg = 'Erro! Filme inválido! Tente novamente!'

    objReturn = {}
    objReturn['msg'] = msg
    objReturn['error'] = error
    return objReturn
