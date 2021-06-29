from flask_restful import Resource
from flask import request


class GenresController(Resource):
    def get(self, genre_id=None):
        from shared.api_return import api_return
        from models.genres.genres import getGenres

        ret = getGenres(genre_id)

        return api_return('Gênero(s) pesquisado(s) corretamente!', False, ret)

    def post(self):
        from models.genres.genres import insertGenres

        genre = request.form.get('genre')
        ret = insertGenres(genre)
        return ret

    def put(self, genre_id):
        # editar generos
        from shared.api_return import api_return
        from models.genres.genres import updateGenres

        genreName = request.form.get('genre')

        genre = {}
        genre['genre_id'] = genre_id
        genre['name'] = genreName

        ret = updateGenres(genre)

        return api_return(ret['msg'], ret['error'])

    def delete(self, genre_id):
        from shared.api_return import api_return
        from models.genres.genres import deleteGenres

        ret = deleteGenres(genre_id)

        return api_return(ret['msg'], ret['error'])
