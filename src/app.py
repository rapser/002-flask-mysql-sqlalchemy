from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_restplus import Api, fields, Resource

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root1983@localhost/flaskmysql'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

db = SQLAlchemy(app)
ma = Marshmallow(app)
#api = Api()
api = Api(app, version='1.0', title='Rapser API',
    description='A simple rest API')
#api.init_app(app)

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

#  Api Rest with Swagger

model = api.model('demo',{
    'name':fields.String('Enter Name'),
    'email':fields.String('Enter Email'),
    'password':fields.String('Enter Password')
})

@api.route('/get')
class getdata(Resource):
    def get(self):
        return {'message':'listado de tareas'}

@api.route('/post')
class postdata(Resource):
    @api.expect(model)
    def post(self):
        return {'message':'data added to database'}

@api.route('/put/<int:id>')
class putdata(Resource):
    @api.expect(model)
    def put(self,id):
        return {'message':'data updated'}

@api.route('/delete/<int:id>')
class deletedata(Resource):
    def delete(self,id):
        return {'message':'data deleted successfully'}


if __name__ == "__main__":
    app.run(debug=True)