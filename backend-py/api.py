# Import framework
from flask import Flask
from flask_restful import Api
from controllers.movies.movies import MoviesController
from controllers.genres.genres import GenresController

# Instantiate the app
app = Flask(__name__)
api = Api(app)

#class CuteKitty(Resource):
#    def get(self): return {}
#    def post(self): return {}
#    def put(self): return {}
#    def delete(self): return None, 204
#    def meow(self): return {}
#api.add_resource(CuteKitty,'/api/kitty/meow',endpoint='meow',methods=['GET'])

# Create routes
# To Do = ver se consegue colocar tipo nos parametros de rota
api.add_resource(MoviesController, '/api/movies/', '/api/movies/<movie_id>')
api.add_resource(GenresController, '/api/genres/', '/api/genres/<genre_id>')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
