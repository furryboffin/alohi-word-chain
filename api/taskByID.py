from flask_restful import Resource
import logging as logger

class TaskByID(Resource):

    def get(self, taskId):
        try:
            logger.debug("GET Method of TaskByID taskID= {}".format(taskId))
            return {"message":"Inside GET Method of TaskByID", "id":int(taskId)},200
        except ValueError:
            logger.error("failed to parse int.")
            return {"message":"Error in GET Method of TaskByID, failed to parse ID, it should be an integer."},400
        except:
            logger.error("failed to parse int with some uknown error.")
            return {"message":"Internal Server Error in GET Method of TaskByID."},500

    def post(self):
        logger.debug("POST Method of TaskByID")
        return {"message":"Inside POST Method of TaskByID"},200

    def put(self):
        logger.debug("PUT Method of TaskByID")
        return {"message":"Inside PUT Method of TaskByID"},200

    def delete(self):
        logger.debug("DELETE Method of TaskByID")
        return {"message":"Inside DELETE Method of TaskByID"},200


