from flask_restful import Resource

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

    def post(self, moviesObject=dict):
        #from shared.api_return import api_return
        #from models.movies.movies import createMovies
        return moviesObject
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
