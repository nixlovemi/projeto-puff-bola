# Observatory Service

# Import framework
from flask import Flask
from flask_restful import Resource, Api
from flask import request

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

class Teste(Resource):
    def get(self):
        return {
            'Galaxies': [
                'Milkyway',
                'Andromeda',
                'Large Magellanic Cloud (LMC)',
                'Small Magellanic Cloud (SMC)'
            ]
        }
    def post(self):
        #teste = request.args.get('teste')
        #teste = request.form.get('teste')

        return {
            'cadastrou': teste
        }

# Create routes
api.add_resource(Teste, '/api/galaxies')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
