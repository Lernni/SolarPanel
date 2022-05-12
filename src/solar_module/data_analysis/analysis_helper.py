class AnalysisHelper:

  def separate_metrics(records, filter = None) -> object:
    if filter is None:
      separated_metrics = {key: [] for key in records[0].data}
    else:
      separated_metrics = {key: [] for key in filter}

    for record in records:
      for key in separated_metrics:
        separated_metrics[key].append(record.data[key])

    return separated_metrics