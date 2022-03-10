from dask import dataframe as dd
import pandas as pd

from globals import DB_PATH

columns = {
  'timestamp': pd.Series(dtype = 'datetime64[s]'),
  'voltage': pd.Series(dtype = 'float64'),
  'input_current': pd.Series(dtype = 'float64'),
  'output_current': pd.Series(dtype = 'float64'),
  'soc': pd.Series(dtype = 'float64'),
}


def init():
  DB_PATH.mkdir(parents=True, exist_ok=True)


def load():
  return dd.read_parquet(DB_PATH)


def append_records(record_list):

  df = dd.from_pandas(pd.DataFrame(record_list, columns = columns), npartitions = 1)
  df.set_index('timestamp')
  dd.to_parquet(df, DB_PATH, append=True, ignore_divisions=True)

  return True