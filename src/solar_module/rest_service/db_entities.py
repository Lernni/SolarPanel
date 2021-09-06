from datetime import datetime

from flask_restx import Resource

from data_access.database_handler import DatabaseHandler

class DBEntities(Resource):
  def get(self):
    ranges = []
    covered = False
    sorted_entitites = sorted(DatabaseHandler.entities, key = lambda e: e.interval, reverse = True)

    for entity in sorted_entitites:
      covered = False
      for entity_range in ranges:
        if entity_range.covers(entity.range):
          covered = True
          break

      if not covered:
        entity_range = entity.range
        ranges.append(entity_range)

    ranges = [entity_range.toJSON() for entity_range in ranges]      
    return ranges