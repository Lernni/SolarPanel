import logging

import numpy as np

from config.config import Config
from globals import MIN_VOLTAGE_AVG, MAX_VOLTAGE_STD, MAX_CURRENT_STD, MAX_CURRENT_DIFF

class CapacityCorrection:

  def run(resolution: int) -> bool:

    '''
    * Determines a correction value for the input_current if necessary
    * The correction value will help preventing the capacity calculation to exceed its actual maximum
    '''

    # TODO: prevent circular import
    from data_access.record_handler import RecordHandler

    # get average record for given resolution
    avg_record = RecordHandler.get_latest_record(resolution)

    # check if present correction value is below the threshold
    with Config() as parser:
      capacity_correction = parser.getfloat('battery_state', 'capacity_correction')
    
    current_diff = avg_record.data['input_current'] - capacity_correction - avg_record.data['output_current']
    logging.debug("Current difference: %f", current_diff)
    
    if current_diff <= MAX_CURRENT_DIFF:
      logging.debug("Current difference is low enough")
      return False

    # -> current difference is too high
    logging.debug("Current difference is too high")


    # get raw records for given time period
    # get all records that make up the average record for the given resolution
    record_list = RecordHandler.get_latest_records(resolution, 1)


    # check if average output_current is smaller than average input_current
    if avg_record.data['output_current'] > avg_record.data['input_current']:
      # capacity correction is applied only as a additional constant to the input_current
      logging.debug("output_current is higher than input_current")
      return False

    # -> input_current is higher than output_current
    logging.debug("input_current is higher than output_current")


    # check if voltage is high and constant enough
    logging.debug(record_list)
    voltage_std = np.std([record.data['voltage'] for record in record_list])
    logging.debug("Voltage standard deviation: %f", voltage_std)

    if avg_record.data['voltage'] < MIN_VOLTAGE_AVG or voltage_std > MAX_VOLTAGE_STD:
      logging.debug("voltage average is too low or voltage value is not constant enough")
      return False

    # -> voltage has a constant high value
    # -> battery is fully charged
    logging.debug("voltage has a constant high value")


    # check if currents are constant enough
    input_current_std = np.std([record.data['input_current'] for record in record_list])
    output_current_std = np.std([record.data['output_current'] for record in record_list])
    logging.debug("Input current standard deviation: %f", input_current_std)
    logging.debug("Output current standard deviation: %f", output_current_std)

    if input_current_std > MAX_CURRENT_STD or output_current_std > MAX_CURRENT_STD:
      logging.debug("currents not constant enough")
      return False

    # -> currents are constant enough
    # -> currents should be equal
    # => capacity correction can be applied
    logging.debug("currents are constant enough")


    capacity_correction = avg_record.data['input_current'] - avg_record.data['output_current']
    with Config() as parser:
      parser.set('battery_state', 'capacity_correction', str(capacity_correction))

    return True