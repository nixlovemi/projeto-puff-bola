from shared.database import getConnection
from datetime import datetime

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
  if genre == None or not genre.isalpha() or len(genre) > 30:
    genre = ''
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



