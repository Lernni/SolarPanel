from time import sleep
import shutil

from dask import dataframe as dd
import pandas as pd

from globals import DB_PATH, DB_TEMP_PATH

columns = {
  'timestamp': pd.Series(dtype = 'datetime64[s]'),
  'voltage': pd.Series(dtype = 'float64'),
  'input_current': pd.Series(dtype = 'float64'),
  'output_current': pd.Series(dtype = 'float64'),
  'soc': pd.Series(dtype = 'float64'),
}

dask_busy = False

def init():
  DB_PATH.mkdir(parents=True, exist_ok=True)


def load():
  return dd.read_parquet(DB_PATH)


def repartition():
  global dask_busy

  if not dask_busy:
    try:
      df = dd.read_parquet(DB_PATH)
      df = df.repartition(freq="1W")
      dd.to_parquet(df, DB_TEMP_PATH)

      shutil.rmtree(DB_PATH)
      shutil.move(DB_TEMP_PATH, DB_PATH)
    except: pass


def append_records(record_list):
  global dask_busy
  while (dask_busy):
    sleep(0.05)

  dask_busy = True
  df = dd.from_pandas(pd.DataFrame(record_list, columns = columns), npartitions = 1)
  df = df.set_index("timestamp", sorted=True)
  dd.to_parquet(df, DB_PATH, append=True)
  dask_busy = False

  return True