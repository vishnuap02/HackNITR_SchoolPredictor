from flask import Flask
from flask_restful import reqparse, abort, Api, Resource , request
import json
import pymongo

app = Flask(__name__)
api = Api(app)


def connect_db():
    client = pymongo.MongoClient('mongodb://localhost:27017')
    dbname = client['hacknitr']
    return dbname
    # Now get/create collection name (remember that you will see the database in your mongodb cluster only after you create a collection)

def abort_if_todo_doesnt_exist(todo_id):
    dbname = connect_db()
    collection_name = dbname["school"]
    # collection name is like a table
    if todo_id not in collection_name:
        abort(404, message="Todo {} doesn't exist".format(todo_id))

parser = reqparse.RequestParser()
parser.add_argument('task')


# Todo
# shows a single todo item and lets you delete a todo item
class school(Resource):
    def get(self, todo_id):
        abort_if_todo_doesnt_exist(todo_id)
        dbname = connect_db()
        collection_name = dbname["school"]
        return collection_name[todo_id]

    def delete(self, todo_id):
        # abort_if_todo_doesnt_exist(todo_id)
        # del TODOS[todo_id]
        return '', 204

    # def put(self, todo_id):
        # args = parser.parse_args()
        # task = {'task': args['task']}
        # TODOS[todo_id] = task
        # return task, 201


# TodoList

class TodoList(Resource):
        def post(self):

                dbname = connect_db()
                collection_name = dbname["school"]
                data = request.get_json()
                # let's create two documents
                school_data = {}
                school_data["school_name"] = data["school_name"]
                # school_data["address"] = data["address"]
                # school_data["city"] = data["city"]
                # school_data["pin_code"] = data["pin_code"]
                # school_data["ph_no"] = data["ph_no"]
                # school_data["is_main_branch"] = data["is_main_branch"]
                # school_data["email"] = data["email"]
                # school_data["school_number"] = data["school_number"]

                collection_name.insert_one(school_data)
                return collection_name, 201

##
## Actually setup the Api resource routing here
##
api.add_resource(TodoList, '/todos')
# api.add_resource(Todo, '/todos/<todo_id>')


if __name__ == '__main__':
    app.run(debug=True)