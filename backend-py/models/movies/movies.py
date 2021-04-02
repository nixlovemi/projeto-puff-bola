def getMovies(movie_id=None):
    from shared.database import getConnection

    mydb = getConnection()
    mycursor = mydb.cursor()

    sql  = " SELECT id, title, isan, trailer_url, duration, release_year, active "
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
