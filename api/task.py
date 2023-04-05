from flask_restful import Resource
import logging as logger

class Task(Resource):

    def get(self):
        logger.debug("GET Method")
        return {"message":"Inside GET Method"},200

    def post(self):
        logger.debug("POST Method")
        # logger.debug(self.dispatch_request.)
        return {"message":"Inside POST Method"},200

    def put(self):
        logger.debug("PUT Method")
        return {"message":"Inside PUT Method"},200

    def delete(self):
        logger.debug("DELETE Method")
        return {"message":"Inside DELETE Method"},200


