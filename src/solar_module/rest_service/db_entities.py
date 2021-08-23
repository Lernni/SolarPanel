from datetime import datetime

from flask_restx import Resource

from data_access.database_handler import DatabaseHandler

class DBEntities(Resource):
    def get(self):
        ranges = []
        for entity in DatabaseHandler.entities:
            entity_range = entity.range.toJSON()
            ranges.append(entity_range)
            
        return ranges