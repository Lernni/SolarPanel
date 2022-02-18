from datetime import datetime

from flask_restx import Resource, reqparse

from data_access.database_handler import df
import pandas as pd

parser = reqparse.RequestParser()
parser.add_argument("start_date")
parser.add_argument("end_date")
parser.add_argument("frequency", type=int)

class DBEntities(Resource):
  def get(self):
    args = parser.parse_args()
    frequency = args["frequency"]
    start_date = args["start_date"]
    end_date = args["end_date"]

    offset = pd.DateOffset(seconds = frequency)
    all_values = pd.Series(data = pd.data_range(
      start = start_date,
      end = end_date,
      freq = offset
    ))

    offset_df = df.index.loc[start_date : end_date].asfreq(freq = offset)
    masked_values = all_values.isin(offset_df[0].values)
    masked_df = all_values[~masked_values]

    # TODO: make timestamp datetime64[s] format




    # ranges = []
    # covered = False
    # sorted_entitites = sorted(DatabaseHandler.entities, key = lambda e: e.interval, reverse = True)

    # for entity in sorted_entitites:
    #   covered = False
    #   for entity_range in ranges:
    #     if entity_range.covers(entity.range):
    #       covered = True
    #       break

    #   if not covered:
    #     entity_range = entity.range
    #     ranges.append(entity_range)

    # ranges = [entity_range.toJSON() for entity_range in ranges]      
    return ranges