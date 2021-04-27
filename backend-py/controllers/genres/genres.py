from flask_restful import Resource
from flask import request

class GenresController(Resource):
  def get(self, genre_id = None):
    from shared.api_return import api_return
    from models.genres.genres import getGenres

    if genre_id is not None:
      ret = getGenres(genre_id)
    else:
      ret = getGenres()

    return api_return('Gênero(s) pesquisado(s) corretamente!', False, ret)

  def post(self):
    from models.genres.genres import insertGenres

    genre = request.form.get('genre')
    ret = insertGenres(genre)
    return ret
