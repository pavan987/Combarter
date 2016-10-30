from flask import Flask
from flask_restful import reqparse, abort, Api, Resource
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)
api = Api(app)



users = { 'users': [
    {
    "id":'1',
    "first_name":"Sherlock",
    "last_name":"Holmes",
    "email":"sherlock@example.com",
    "apt":"Apt 23-47"
    },
    {
    "id":'2',
    "first_name":"Pavan",
    "last_name":"gondhi",
    "email":"gondhi@ysc.com",
    "apt":"Apt 43-44"
    }
    ]
}


buildings = { 'buildings': [
{
   "id":'1',
   "title":"Mardi Gras",
   "address":"720 W 27th Street",
   "city":"Los Angeles",
   "state":"CA",
   "zip":"90007",
   "desc": "Situated on the out-skirts, provides a perfect mix of natural living.",
   "img":"http://g.mnp0.com/gimg/34.028389/-118.279537.jpg"
},

{
   "id":'2',
   "title":"Nupac Apartments",
   "address":"450 W 28th Street",
   "city":"San Diego",
   "state":"CA",
   "zip":"90090",
   "desc": "Affordable Student housing within walking distance to University of Southern California",
   "img":"https://www.nupac.com/img/large-640-400/2618-side-view.png"

},

{
   "id":'3',
   "title":"First Choice Hosuing",
   "address":"908 W Adams Blvd",
   "city":"Los Angeles",
   "state":"CA",
   "zip":"90247",
   "desc": "First Choice Housing Association provides quality accommodation solutions for students",
   "img":"http://stuho.com/Pictures/large/Bcode/1-01.jpg"

},

{
   "id":'4',
   "title":"Stuho",
   "address":"2650 Orhchard Avenue",
   "city":"Pasadena",
   "state":"CA",
   "zip":"90089",
   "desc": "We offer all types of USC Student Housing: Apartments, Houses, Rooms at affordable rates",
   "img":"http://stuho.com/Pictures/large/Bcode/1-01.jpg"

},

{
   "id":'5',
   "title":"Nupac Apartments",
   "address":"2656 Ellendale",
   "city":"Sacramento",
   "state":"CA",
   "zip":"90124",
   "desc": "Affordable Student housing within walking distance to University of Southern California",
   "img":"https://www.nupac.com/img/large-640-400/2618-side-view.png"

}


]
}

join = {'requests':{}}
my_profile={
    "user" : {
    "id" : 1,
    "first_name": "Rahul",
    "last_name": "Desai",
    "email": "rahul@example.com",
    "apt" : "Apt x"
},
"building":{
    "id":2,
    "title":"Trilok Leaf",
    "desc": "Situated on the out-skirts, provides a perfect mix of natural living.",
    "img":"https://enlightenme.com/images/2014/06/Apartment-vs.-Condo-What%E2%80%99s-the-Difference-670x442.jpg"
}
}



pool_user_rel={('1','1'):'pending'}
owner_noti={}
carpool_requests={
    '1' : [{
        "id":1,
        "status":"pending",
        "where":"McClinctok Ave",
        "when":"2016-03-11",
        "owner":{
            "id":2,
            "first_name":"Kartik",
            "last_name":"Desai"
        }
    }]
}

temp_carpools = {
    "results" : [
        {
            "id":'1',
            "where":"Viva Technologies, 26th W Street",
            "when":"2016-30-10",
            "max_occupancy":3,
            "owner":{
                "id":"2",
                "first_name":"Mehul",
                "last_name":"Lispov"
            }
        },
        {
            "id": '2',
            "where":"2652 Ellendale Place",
            "when":"2016-02-11",
            "max_occupancy":5,
            "owner":{
                "id":"3",
                "first_name": "Matt",
                "last_name": "Damon"
            }
        }
    ]
}

def abort_if_apartment_doesnt_exist(apt_id):
    if apt_id not in buildings:
        abort(404, message="Apartment {} doesn't exist".format(apt_id))



# shows a single todo item and lets you delete a todo item
class Apt(Resource):
    def get(self, apt_id):
        abort_if_apartment_doesnt_exist(apt_id)
        return buildings[apt_id]

# shows a list of all todos, and lets you POST to add new tasks
class AptList(Resource):
    def get(self):
        return buildings

class UserJoin(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user')
        args = parser.parse_args()
        user = args['user']
        if user in join['requests']:
            return join['requests'][user]
        else:
            return {'status':'None',"message":"User not part of apartment"}


    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('user')
        parser.add_argument('building')
        parser.add_argument('status')
        args = parser.parse_args()
        user = args['user']
        status = args['status']
        if status == 'pending':
            join['requests'][user]={'status':'pending',"message":"Owner did not approve yet"}
        if status =='approved':
            for b in buildings['buildings']:
                if args['building'] == b['id']:
                    my_profile['building']=b
            for u in users['users']:
                if args['user']== u['id']:
                    my_profile['user']=users
            join['requests'][user] = {'status': 'approved', "message": "Owner approved to join"}

        return {"status":"success","message":"Request sent successfully!"}

class MyProfile(Resource):
    def get(self):
        return my_profile

class User(Resource):
    def get(self):
        return users

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        parser.add_argument('email')
        parser.add_argument('apt')
        args = parser.parse_args()
        count=0
        for i in users['users']:
            if args['id'] == i['id']:
                for key,value in args.items():
                    if value:
                        users['users'][count][key]=value
                return {"status": "success"}
            count += 1



class BuildingSearch(Resource):
    def get(self,name):
        search_results = {'status':'failure','results':[]}
        flag = 0
        if name.strip() == '':
            flag = 1
            search_results['status'] ='success'
            search_results["results"]= buildings['buildings']
        else:
            for value in buildings['buildings']:
                if name in value['id'] or name.lower() in value['title'].lower() or name.lower() in value['city'].lower() \
                        or name.lower() in value['state'].lower() or  name in value['zip']:
                    flag = 1
                    search_results["results"].append(value)
        if flag == 1:
            search_results['status'] ='success'
        return search_results

class TempCarPool(Resource):
    def get(self):
        return temp_carpools

    def post(self):

        parser = reqparse.RequestParser()
        parser.add_argument('where')
        parser.add_argument('when')
        parser.add_argument('max_occupancy')
        parser.add_argument('owner')
        args = parser.parse_args()
        id = len(temp_carpools['results'])
        temp_carpools['results'].append({'id':id})
        for key,value in args.items():
            if key == 'owner':
                for u in users['users']:
                    if value == u['id']:
                        value = {'id':u['id'],'firstname':u['first_name'],'last_name':u['last_name']}
            temp_carpools['results'][id][key]=value
        return {'status':'success'}


class CarPoolRequests(Resource):
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id')
        args = parser.parse_args()
        if args['id'] in carpool_requests:
            return {'results' : carpool_requests[args['id']] }
        else:
            return {}

    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_user')
        parser.add_argument('id_carpool')
        parser.add_argument('id_owner')
        parser.add_argument('status')
        args = parser.parse_args()
        id_user = args['id_user']
        id_carpool = args['id_carpool']
        id_owner = args['id_owner']
        if args['status'] == 'join':
            pool_user_rel[(id_user, id_carpool)]='pending'
            if id_owner not in owner_noti:
                owner_noti[id_owner]=[]
                id=0
            else:
                id = len(owner_noti[id_owner])
            owner_noti[id_owner].append({'id':id,'id_carpool':id_carpool ,'id_user': id_user})
            if id_user not in carpool_requests:
                print id_user
                carpool_requests[id_user]=[]
                id=0
            else:
                id = len(carpool_requests[id_user])
            for c in temp_carpools['results']:
                print c
                if c['id'] == id_carpool:
                    print "entered"
                    carpool_requests[id_user].append({'id':id, 'id_carpool':id_carpool,'status':'pending','where':c['where'],
                                                      'when':c['when'], 'owner':c['owner'] })
        return { "status":"success", "message":"Request sent successfully!"}





class PoolUserStatus(Resource):

    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_user')
        parser.add_argument('id_carpool')
        args = parser.parse_args()
        if  (args['id_user'],args['id_carpool']) in pool_user_rel:
            return {'status':pool_user_rel[(args['id_user'],args['id_carpool'])]}
        else:
            return {'status':'None'}


class OwnerNotifications(Resource):
    def get(self,user):
        if user in owner_noti:
            return owner_noti[user]
        else:
            return {}

class OwnerAction(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('id_owner')
        parser.add_argument('id_noti')
        parser.add_argument('action')
        args = parser.parse_args()
        action = args['action']
        owner = args['id_owner']
        id = args['id_noti']
        id_user =None
        id_carpool=None
        for n in owner_noti[owner]:
            if n['id'] == id:
                id_user=n['id_user']
                id_carpool=n['id_carpool']
                pool_user_rel[(id_user,id_carpool)]=action
        count = 0
        for r in carpool_requests[id_user]:
            if r['id_carpool'] == id_carpool:
                carpool_requests[id_user][count]['status'] = action
        return { "status":"success", "message":"Request sent successfully!"}

        # if action == 'approved':
        #     count=0
        #     for c in temp_carpools['results']:
        #         if c['id']==id_carpool:
        #             max_oc = temp_carpools['results'][count]['max_occupancy']
        #             temp_carpools['results'][count]['max_occupancy'] = max_oc +1
        #





class Notifications(Resource):
    def get(self,user):
        if user in notifications:
            return {'results': notifications[user]}
        else:
            return {'results': []}



api.add_resource(AptList, '/api')
api.add_resource(BuildingSearch, '/api/search/<name>')
api.add_resource(User, '/api/profile')
api.add_resource(UserJoin, '/api/join')
api.add_resource(MyProfile, '/api/me')
api.add_resource(TempCarPool,'/api/tempcarpool')
api.add_resource(PoolUserStatus,'/api/pooluser')
api.add_resource(OwnerNotifications,'/api/ownernoti/<user>')
api.add_resource(OwnerAction,'/api/owneraction')
api.add_resource(CarPoolRequests,'/api/carpool-request')
api.add_resource(Notifications,'/api/notifications/<user>')

if __name__ == '__main__':
    app.run(debug=True)
