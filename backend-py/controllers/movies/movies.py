from flask_restful import Resource
from flask import request

# /api/movies
class MoviesController(Resource):
    def get(self, movie_id=None):
        from shared.api_return import api_return
        from models.movies.movies import getMovies

        if movie_id is not None:
            ret = getMovies(movie_id)
        else:
            ret = getMovies()

        return api_return('Filmes pesquisados corretamente!', False, ret)
    #def patch(self):
    #    from flask import request
    #    teste = request.args.get('teste')
    #    return teste

    def post(self):
      from models.movies.movies import insertMovies
      from shared.api_return import api_return

      title = request.form.get('title')
      genre = request.form.get('genre')
      isan = request.form.get('isan')
      duration = request.form.get('duration')
      releaseYear = request.form.get('releaseYear')
      rating = request.form.get('rating')

      movies = {}
      movies['title'] = title
      movies['genre'] = genre
      movies['isan'] = isan
      movies['duration'] = duration
      movies['releaseYear'] = releaseYear
      movies['rating'] = rating
      ret = insertMovies(movies)

      # trata se tem tds as variaveis q precisa
      # ret = createMovie(Movies)
      # trata o retorno

      return ret
        #return api_return('Filmes adicionado corretamente!', False, ret)
        #teste = request.args.get('teste')
        #teste = request.form.get('teste')

        # mydb = getConnection()
        # mycursor = mydb.cursor()
        # mycursor.execute("SELECT * FROM movies")
        # myresult = mycursor.fetchall()

        # for x in myresult:
        #     return {
        #         'oi': x
        #     }

        #return {
        #    'cadastrou': teste
        #}
