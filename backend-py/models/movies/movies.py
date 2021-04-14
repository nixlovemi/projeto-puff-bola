from shared.database import getConnection
from datetime import datetime

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
        objMovies = {}
        objMovies['id'] = x[0]
        objMovies['title'] = x[1]
        objMovies['isan'] = x[2]
        objMovies['trailer_url'] = x[3]
        objMovies['duration'] = x[4]
        objMovies['release_year'] = x[5]
        objMovies['active'] = x[6]

        arrMovies.append(objMovies)

    return arrMovies

def insertMovies(movie):
  title = movie['title']
  genre = movie['genre']
  isan = movie['isan']
  rating = movie['rating']
  releaseYear = movie['releaseYear']
  duration = movie['duration']

#Tratamento das Variaveis
  if title == None:
    title = ''
  if duration == None or not duration.isnumeric():
    duration = -1
  else:
    duration = int(duration)
  if rating == None or not rating.isnumeric():
    rating = -1
  else:
    rating = int(rating)
  msg = 'Filme Cadastrado com sucesso!'
  error = False
  if genre == None or not genre.isnumeric():
    genre = -1
  else:
    genre = int(genre)
  if releaseYear == None or not releaseYear.isnumeric():
    releaseYear = -1
  else:
    releaseYear = int(releaseYear)
  if isan == None:
    isan = ''
# Validação das Variaveis
  if len(title) > 100 or title == '':
    error = True
    msg = 'Erro! Título Inválido, Insira Título com até 100 caracteres!'
    if genre < 0 and genre > 12:
      error = True
      msg = 'Erro! Favor escolher um Gênero válido'

  mydb = getConnection()
  mycursor = mydb.cursor()
  sql = f'SELECT id FROM genres WHERE id = {genre} AND active = 1'
  mycursor.execute(sql)
  myresult = mycursor.fetchall()

  if len(myresult) == 0:
    error = True
    msg = 'Erro! Gênero inexistente'
  if len(isan) > 100 or isan == '':
    error = True
    msg = 'Erro! Isan inválido! Insira Isan com até 100 caracteres!'
  if duration < 0 or duration > 999:
    error = True
    msg = 'Erro! Duração Inválida!'
  if releaseYear < 1895 or releaseYear > presentYear:
    error = True
    msg = 'Erro! Ano de lançamento inválido!'
  if rating > 10 or rating < 0:
    error = True
    msg = 'Erro! Favor escolher uma nota entre 0 e 10!'

  if not validarISAN(isan):
      error = True
      msg = 'Erro! ISAN inválido!'

#Inserindo Filme na tabela
  if error == False:
    sqlInsert = (f"INSERT INTO movies (title, isan, duration, release_year) VALUES ( '{title}', '{isan}', {duration}, {releaseYear})")
    mycursor.execute(sqlInsert)
    if mycursor.rowcount <= 0:
        error = True
        msg = 'Erro ao adicionar o filme'
    else:
      movieLastId = mycursor.lastrowid
      sqlInsert = (f"INSERT INTO movies_genres (genre_id, movie_id) VALUES ({genre}, {movieLastId}) ")
      mycursor.execute(sqlInsert)

  objReturn = {}
  objReturn['msg'] = msg
  objReturn['error'] = error
  return objReturn

def validarISAN(isan):
    import re
    #x = re.search("/^[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}/gm", isan)
    x = re.search("^[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}\-[a-zA-z0-9]{4}", isan)

    if x:
      return True
    else:
      return False
