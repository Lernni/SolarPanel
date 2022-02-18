from numpy.lib.nanfunctions import _nanpercentile_dispatcher
from globals import DB_PATH
import logging
from dask import dataframe as dd
import pandas as pd

df = None
columns = {
  'timestamp': pd.Series(dtype = 'datetime64[s]'),
  'voltage': pd.Series(dtype = 'float64'),
  'input_current': pd.Series(dtype = 'float64'),
  'output_current': pd.Series(dtype = 'float64'),
  'soc': pd.Series(dtype = 'float64'),
}

pd.set_option('precision', 2)

def load():
  global df
  
  DB_PATH.mkdir(parents=True, exist_ok=True)
  
  try:
    df = dd.read_csv(DB_PATH)

    logging.info("Database loaded")
  except:
    logging.info("No Database found")


def add_record_list(record_list) -> bool:
  global df

  if df is None:
    df = dd.from_pandas(pd.DataFrame(record_list, columns = columns), npartitions = 1)
    df.set_index('timestamp')
  else:
    df = df.append(pd.DataFrame(record_list, columns = columns))

  logging.info(df.dtypes)
  logging.info(df.tail())

  df.to_csv(DB_PATH)

  return True


def get_records(start_date, end_date):
  global df

  return df.loc[start_date:end_date].compute()
