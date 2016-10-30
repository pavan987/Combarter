from flask import Flask
from flask_restful import reqparse, abort, Api, Resource

app = Flask(__name__)
api = Api(app)

Apartments = {
    '1': {'Name': 'Mardigras', 'Address':'720 W 27th Street',  'Zip':'90007'},
    '2' : {'Name': '2607', 'Address':'723 W 27th Street', 'Zip':'90047'},
    '3' : {'Name': 'Marditt', 'Address':' 30 W 27th Street', 'Zip':'90067'}

}


def abort_if_apartment_doesnt_exist(apt_id):
    if apt_id not in Apartments:
        abort(404, message="Apartment {} doesn't exist".format(apt_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# shows a single todo item and lets you delete a todo item
class Apt(Resource):
    def get(self, apt_id):
        abort_if_apartment_doesnt_exist(apt_id)
        return Apartments[apt_id]

# shows a list of all todos, and lets you POST to add new tasks
class AptList(Resource):
    def get(self):
        return Apartments

class AptSearch(Resource):
    def get(self,name):
        search_results = {}
        for key,value in Apartments.items():
            if name in value['Name'] or name in value['Address'] or name in value['Zip'] :
                flag=1
                search_results[key]=value

        return search_results


##
api.add_resource(AptList, '/apt')
api.add_resource(Apt, '/apt/<apt_id>')
api.add_resource(AptSearch, '/apt/search/<name>')


if __name__ == '__main__':
    app.run(debug=True)