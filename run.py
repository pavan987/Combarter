from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)

Apartments = {
  '1':  {'Name': 'MardiGras', 'Address':'720 W 27th Street','City':'Los Angeles','State':'CA','Zip':'90007','image':'http://g.mnp0.com/gimg/34.028389/-118.27'},
  '2' : {'Name': 'Nupac Apartments', 'Address':'450 W 28th Street','City':'San Diego','State':'CA','Zip':'90090','image':'https://www.nupac.com/img/large-640-400/'},
  '3' : {'Name': 'First Choice Housing', 'Address':'908 W Adams Blvd','City':'Los Angeles','State':'CA','Zip':'90247','image':'http://stuho.com/Pictures/large/Bcode/1-'},
  '4' : {'Name': 'Stuho', 'Address':'2650 Orchard Avenue','City':'Pasadena','State':'CA','Zip':'90089','image':'http://stuho.com/Pictures/large/Bcode/1-'},
  '5' : {'Name': 'Nupac', 'Address':'2656 Ellendale','City':'Sacramento','State':'CA','Zip':'90124','image':'http://g.mnp0.com/gimg/34.028389/-118.27'}

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
