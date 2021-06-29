from flask_restful import Resource
from flask import request


# /api/movies
class MoviesController(Resource):
    def get(self, movie_id=None):
        from shared.api_return import api_return
        from models.movies.movies import getMovies

        ret = getMovies(movie_id)

        return api_return('Filme(s) pesquisado(s) corretamente!', False, ret)

    def post(self):
        # inserir filmes
        from shared.api_return import api_return
        from models.movies.movies import insertMovies

        title = request.form.get('title')
        # o genre_id é uma string json nesse formato -> {"indice":id_genre, ...} -> {"0": 10, "1", 20}
        genre_id = request.form.get('genre_id')
        isan = request.form.get('isan')
        trailerUrl = request.form.get('trailerUrl')
        duration = request.form.get('duration')
        releaseYear = request.form.get('releaseYear')
        rating = request.form.get('rating')

        movies = {}
        movies['title'] = title
        movies['genre_id'] = genre_id
        movies['isan'] = isan
        movies['trailerUrl'] = trailerUrl
        movies['duration'] = duration
        movies['releaseYear'] = releaseYear
        movies['rating'] = rating
        ret = insertMovies(movies)

        return api_return(ret['msg'], ret['error'])

    def put(self, movie_id):
        # editar filmes
        from shared.api_return import api_return
        from models.movies.movies import updateMovies

        title = request.form.get('title')
        genre_id = request.form.get('genre_id')
        isan = request.form.get('isan')
        trailerUrl = request.form.get('trailerUrl')
        duration = request.form.get('duration')
        releaseYear = request.form.get('releaseYear')

        movies = {}
        movies['movie_id'] = movie_id
        movies['title'] = title
        movies['genre_id'] = genre_id
        movies['isan'] = isan
        movies['trailerUrl'] = trailerUrl
        movies['duration'] = duration
        movies['releaseYear'] = releaseYear
        ret = updateMovies(movies)

        return api_return(ret['msg'], ret['error'])

    def delete(self, movie_id):
        from shared.api_return import api_return
        from models.movies.movies import deleteMovies

        ret = deleteMovies(movie_id)

        return api_return(ret['msg'], ret['error'])