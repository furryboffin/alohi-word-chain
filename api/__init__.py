from flask_restful import Api
from app import app
from .task import Task
from .taskByID import TaskByID
from .employee import Employee

restServer = Api(app)

restServer.add_resource(Task, "/api/v1.0/task")
restServer.add_resource(TaskByID, "/api/v1.0/task/<string:taskId>")
restServer.add_resource(employee, "/api/v1.0/employee")
