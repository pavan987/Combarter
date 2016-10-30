from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)

buildings = { [
{
    "id":2,
    "title":"Trilok Leaf",
    "desc": "Situated on the out-skirts, provides a perfect mix of natural living.",
    "img":"https://enlightenme.com/images/2014/06/Apartment-vs.-Condo-What%E2%80%99s-the-Difference-670x442.jpg"
},
{
    "id":2,
    "title":"Trilok Leaf",
    "desc": "Situated on the out-skirts, provides a perfect mix of natural living.",
    "img":"https://enlightenme.com/images/2014/06/Apartment-vs.-Condo-What%E2%80%99s-the-Difference-670x442.jpg"
}
]
}


def abort_if_apartment_doesnt_exist(apt_id):
    if apt_id not in buildings:
        abort(404, message="Apartment {} doesn't exist".format(apt_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# shows a single todo item and lets you delete a todo item
class Apt(Resource):
    def get(self, apt_id):
        abort_if_apartment_doesnt_exist(apt_id)
        return buildings[apt_id]

# shows a list of all todos, and lets you POST to add new tasks
class AptList(Resource):
    def get(self):
        return buildings

class BuildingSearch(Resource):
    def get(self,name):
        search_results = {'status':'failure','results':[]}
        flag = 0
        for value in buildings:
            flag=1
            if name in value['id'] or name in value['title'] or name in value['desc']:
                search_results["results"].append(value)
        if flag == 1:
            search_results['status'] ='success'
        return search_results


##
api.add_resource(AptList, '/apt')
api.add_resource(Apt, '/apt/<apt_id>')
api.add_resource(BuildingSearch, '/apt/search/<name>')


if __name__ == '__main__':
    app.run(debug=True)
