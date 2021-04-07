from shared.database import getConnection


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
  if rating.isnumeric():
    rating = int(rating)
  releaseYear = movie['releaseYear']
  duration = movie['duration']
  msg = 'Filme Cadastrado com sucesso!'
  error = False

  if title is None or len(title) == 0:
    error = True
    msg = 'Erro! Favor digitar um Título válido'
  elif len(title) > 100:
    error = True
    msg = 'Erro! Título Inválido, excede a quantidade de 100 caracteres!'
  if genre is None or genre.isnumeric() or len(genre) > 30:
    error = True
    msg = 'Erro! Favor escolher um Gênero válido'
  mydb = getConnection()
  mycursor = mydb.cursor()
  sql = f'SELECT id FROM genres WHERE name = "{genre}" AND active = 1'
  mycursor.execute(sql)
  myresult = mycursor.fetchall()
  if len(myresult) == 0:
    error = True
    msg = 'Erro! Gênero inexistente'
  if isan is None or len(isan) == 0:
    error = True
    msg = 'Erro! Favor inserir um Isan!'
  elif len(isan) > 100:
    error = True
    msg = 'Erro! Isan excede 100 caracteres, favor inserir Isan válido!'
  if duration is not None and not duration.isnumeric():
    error = True
    msg = 'Erro! Duração inválida!'
  elif duration is not None and len(duration) > 5:
    error = True
    msg = 'Erro! Duração excede o tamanho máximo!'
    return 'oi'
  if releaseYear is not None and not releaseYear.isnumeric():
    error = True
    msg = 'Erro! Ano de lançamento inválido!'
    return 'oi'
  elif releaseYear is not None and len(releaseYear) is not 4:
    error = True
    msg = 'Erro! Ano de lançamento precisa ter quatro dígitos!'
    return 'oi'
  if rating is None or rating == '' or rating.isalpha():
    error = True
    msg = 'Erro! Nota inválida!'
  elif rating > 10 or rating < 0:
    error = True
    msg = 'Erro! Favor escolher uma nota entre 0 e 10!'
  objReturn = {}
  objReturn['msg'] = msg
  objReturn['error'] = error
  return objReturn

