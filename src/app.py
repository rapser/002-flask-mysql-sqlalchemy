from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_swagger_ui import get_swaggerui_blueprint
from flask_restful import Api, Resource, fields

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root1983@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)

api = Api(app)

# class AwesomeAPI(Resource):
#     def get(self):
#         '''
#         Get method represents a GET API method
#         '''
#         return {'message': 'My First Awesome API'}

# api.add_resource(AwesomeAPI, '/awesome')

# SWAGGER

class getdata(Resource):
    def get(self):
        return {'message': "trabajando"}

class postdata(Resource):
    def post(self):
        return {'message': "trabajando"}

class putdata(Resource):
    def put(self, id):
        return {'message': id}

class deletedata(Resource):
    def delete(self, id):
        return {'message': id}

api.add_resource(getdata, '/get')
api.add_resource(postdata, '/post')
api.add_resource(putdata, '/put/<int:id>')
api.add_resource(deletedata, '/delete/<int:id>')

# API REST
 
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(70), unique=True)
    description = db.Column(db.String(100))

    def __init__(self, title, description):
        self.title = title
        self.description = description

db.create_all()

class TaskSchema(ma.Schema):
    class Meta:
        fields = ('id','title','description')

task_schema = TaskSchema()
tasks_schema = TaskSchema(many=True)

@app.route('/tasks', methods=['POST'])
def create_task():

    title = request.json['title']
    description = request.json['description']

    new_task = Task(title,description)
    db.session.add(new_task)
    db.session.commit()
    return task_schema.jsonify(new_task)

@app.route('/tasks', methods=['GET'])
def get_task():
    all_tasks = Task.query.all()
    result = tasks_schema.dump(all_tasks)
    return jsonify(result)

@app.route('/tasks/<id>', methods=['GET'])
def get_task_byId(id):
    task = Task.query.get(id)
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['PUT'])
def update_task(id):
    task = Task.query.get(id)

    title = request.json['title']
    description = request.json['description']
    
    task.title = title
    task.description = description

    db.session.commit()
    return task_schema.jsonify(task)

@app.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    db.session.delete(task)
    db.session.commit()

    return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Bienvenidos al API"})

if __name__ == "__main__":
    app.run(debug=True)