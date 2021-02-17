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

name_space = api.namespace('tasks', description='Tasks APIs')
name_space2 = api.namespace('product', description='Tasks APIs')

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

# @app.route('/tasks', methods=['POST'])
# def create_task():
#     title = request.json['title']
#     description = request.json['description']
#     new_task = Task(title,description)
#     db.session.add(new_task)
#     db.session.commit()
#     return task_schema.jsonify(new_task)

# @app.route('/tasks', methods=['GET'])
# def get_task():
#     all_tasks = Task.query.all()
#     result = tasks_schema.dump(all_tasks)
#     return jsonify(result)

# @app.route('/tasks/<id>', methods=['GET'])
# def get_task_byId(id):
#     task = Task.query.get(id)
#     return task_schema.jsonify(task)

# @app.route('/tasks/<id>', methods=['PUT'])
# def update_task(id):
#     task = Task.query.get(id)
#     title = request.json['title']
#     description = request.json['description']    
#     task.title = title
#     task.description = description
#     db.session.commit()
#     return task_schema.jsonify(task)

# @app.route('/tasks/<id>', methods=['DELETE'])
# def delete_task(id):
#     task = Task.query.get(id)
#     db.session.delete(task)
#     db.session.commit()
#     return task_schema.jsonify(task)

@app.route('/', methods=['GET'])
def index():
    return jsonify({"message":"Bienvenidos al API"})

#  Api Rest with Swagger

model = api.model('Task',{
    'title':fields.String,
    'description':fields.String
})

resource_fields = api.model('Peru', {
    'title': fields.String,
    'description': fields.String
})

@name_space.route("")
@name_space.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error' })
class getdata(Resource):
    def get(self):
        '''Lista todas las tareas'''
        all_tasks = Task.query.all()
        result = tasks_schema.dump(all_tasks)
        return jsonify(result)  
    @api.expect(resource_fields)
    def post(self):
        '''Crea una tarea'''
        title = request.json['title']
        description = request.json['description']
        new_task = Task(title,description)
        db.session.add(new_task)
        db.session.commit()
        return task_schema.jsonify(new_task)

@name_space.route("/<int:id>")
@name_space.doc(responses={ 200: 'OK', 400: 'Invalid Argument', 500: 'Mapping Key Error'})
class putdata(Resource):
    def get(self,id):
        '''Obtiene una tarea segun su id'''
        task = Task.query.get(id)
        return task_schema.jsonify(task)
    @api.expect(model)
    def put(self,id):
        '''Actualizar una tarea segun su id'''
        task = Task.query.get(id)
        title = request.json['title']
        description = request.json['description']
        task.title = title
        task.description = description
        db.session.commit()
        return task_schema.jsonify(task)
    def delete(self,id):
        '''Eliminar una tarea segun su id'''
        task = Task.query.get(id)
        db.session.delete(task)
        db.session.commit()
        return task_schema.jsonify(task)

if __name__ == "__main__":
    app.run(debug=True)