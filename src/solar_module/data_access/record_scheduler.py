import time
from threading import Thread

import schedule

from data_analysis.tasks.average_calculation import AverageCalculationTask


class RecordScheduler(Thread):

  '''
  * Schedules creation of new records exactly once per second
  * Schedules calculation of averages once per day at midnight
  '''

  def __init__(self, job):
    Thread.__init__(self)
    self.name = "RecordScheduler"
    self.running = True
    self.job = job

    self.calc_averages_job = schedule.every().day.at("00:00").do(RecordScheduler.run_threaded, AverageCalculationTask)
  

  def run_threaded(job_func):
    job_thread = Thread(target = job_func, name= "JobThread")
    job_thread.start()

  def run(self):
    while self.running:
      # sleep as long as needed to run at an exact one second interval
      self.job()
      schedule.run_pending()
      time.sleep(1.0 - time.time() % 1.0)

  def stop(self):
    self.running = False
    schedule.cancel_job(self.calc_averages_job)