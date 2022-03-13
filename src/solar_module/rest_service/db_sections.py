from datetime import datetime

from flask_restx import Resource, reqparse
import pandas as pd
import numpy as np

import data_access.database_handler as db


parser = reqparse.RequestParser()
parser.add_argument("start_time")
parser.add_argument("end_time")


class DBSections(Resource):
  def get(self):
    args = parser.parse_args()

    # convert timestamps from frontend to pandas datetime objects
    start_time = pd.to_datetime(datetime.fromtimestamp(int(args["start_time"]) / 1000))
    end_time = pd.to_datetime(datetime.fromtimestamp(int(args["end_time"]) / 1000))

    db.repartition()
    df = db.load()

    mask = (
      (df.index >= start_time) &
      (df.index <= end_time)
    )

    # locate requested timestamps that meet condition of mask
    marked_frame = df.loc[mask, []].compute()
    marked_frame = marked_frame.reset_index()

    # group all continuous sections of timestamps
    marked_frame["gap"] = marked_frame["timestamp"].diff().dt.seconds > 1
    marked_frame["gap"] = marked_frame["gap"].cumsum()

    # get start and end time of each section
    gk = marked_frame.groupby("gap").agg({"timestamp" : [np.min, np.max]})

    # convert gk dataframe to 2D array of unix timestamps
    record_groups = gk.to_numpy().astype("datetime64[s]").astype("int").tolist()
    return record_groups