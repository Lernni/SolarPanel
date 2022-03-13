from datetime import datetime

from flask_restx import Resource, reqparse
import pandas as pd
import numpy as np

import data_access.database_handler as db


MAX_RECORDS = 150

parser = reqparse.RequestParser()
parser.add_argument("start_time")
parser.add_argument("end_time")
parser.add_argument("units[]", action="append")


class DBRecords(Resource):
  def get(self):
    args = parser.parse_args()
    units = args["units[]"]
    
    # convert timestamps from frontend to pandas datetime objects
    start_time = pd.to_datetime(datetime.fromtimestamp(int(args["start_time"]) / 1000))
    end_time = pd.to_datetime(datetime.fromtimestamp(int(args["end_time"]) / 1000))

    db.repartition()
    df = db.load()

    mask = (
      (df.index >= start_time) &
      (df.index <= end_time)
    )

    # locate requested records that meet condition of mask
    marked_frame = df.loc[mask, units]

    # check if the requested time range contains any records
    if len(marked_frame.index) == 0: return []

    # resample records to match the requested time interval, if necessary
    if len(marked_frame.index) > MAX_RECORDS:
      resample_freq = len(marked_frame.index) // MAX_RECORDS
      marked_frame = marked_frame.compute().resample(str(resample_freq) + "S").mean()

      # drop nan rows from resampled dataframe
      marked_frame = marked_frame.dropna()

      # find gaps in resampled dataframe
      marked_frame["timestamp"] = marked_frame.index
      marked_frame["gap"] = marked_frame["timestamp"].diff().dt.seconds > resample_freq
      marked_frame["gap"] = marked_frame["gap"].cumsum()

    # get row indices where each section starts (where gaps occur)
    split_rows = marked_frame.groupby("gap")["timestamp"].count().cumsum().tolist()

    # make dataframe structure and types ready for expected data format
    marked_frame = marked_frame[units].reset_index()
    marked_frame["timestamp"] = marked_frame["timestamp"].values.astype("datetime64[s]").astype("int")
    marked_frame[units] = marked_frame[units].applymap('{:,.2f}'.format)

    # split dataframe into sections and convert them to lists
    marked_frames = np.split(marked_frame, split_rows, axis=0)
    requested_list = []
    for i in range(len(marked_frames) - 1):
      requested_list.append(marked_frames[i].to_numpy().tolist())

    return requested_list