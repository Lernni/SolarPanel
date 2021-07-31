from data_access.globals import DB_PATH
from data_access.data_entity import DataEntity
from data_objects.date_time_range import DateTimeRange

import logging

class DatabaseHandler:

    entities = []
    current_entity = None
    RECORD_LIMIT = 40

    def init():

        # check folder structure
        DB_PATH.mkdir(parents = True, exist_ok = True)

        # list of all csv files in folder
        csv_files = [f for f in DB_PATH.iterdir() if f.suffix == '.csv']

        # analyze and check database
        DatabaseHandler.entities = [DataEntity(f) for f in csv_files]

    def new_entity():
        DatabaseHandler.current_entity = DataEntity()

    def del_entity():
        DatabaseHandler.current_entity = None

    def add_records(records) -> bool:
        if DatabaseHandler.current_entity is None:
            raise Exception('No entity selected')

        if DatabaseHandler.current_entity.record_count + len(records) > DatabaseHandler.RECORD_LIMIT:
            place_remaining = DatabaseHandler.RECORD_LIMIT - DatabaseHandler.current_entity.record_count
            if len(records[:place_remaining]) != 0:
                DatabaseHandler.current_entity.add_records(records[:place_remaining])
                records = records[place_remaining:]

                DatabaseHandler.current_entity = DataEntity()
                return DatabaseHandler.add_records(records)
            else:
                DatabaseHandler.current_entity = DataEntity()
                return True
        else:
            return DatabaseHandler.current_entity.add_records(records)
        

    def get_records(start_date_time, end_date_time, interval = 1):
        time_frame = [
            [DateTimeRange(start_date_time, end_date_time), None]
        ]

        # find entities that have data in the requested time frame
        # try to include entities that have an interval divisible by the requested interval
        # this minimizies load when compromising records to the given interval

        divider_intervals = ((interval % 2) == 0)

        # sort entities by interval
        # entities with the highest interval will be processed first
        # entities that have a lower interval and cover the same time frame as a higher interval entity will be ignored

        sorted_entitites = sorted(DatabaseHandler.entities, key = lambda e: e.interval)

        for sorted_entity in sorted_entitites:
            if sorted_entity.start_date_time > end_date_time or \
                sorted_entity.end_date_time < start_date_time or \
                sorted_entity.interval > interval: continue

            if divider_intervals:
                if ((interval % sorted_entity.interval) != 0): continue
            else:
                if (interval != sorted_entity.interval): continue

            # loop through already applied entities to see if the current entity can be applied to cover gaps in the requested time frame
            # if a gap is found, apply the entity to fill the gap
            
            i = 0
            while i < len(time_frame):
                if time_frame[i] is None:
                    fillable_section = time_frame[i][0].intersect(sorted_entity.date_time_range)
                    if fillable_section is not None:
                        new_sections = time_frame[i][0].split_merge(sorted_entity.date_time_range)

                        del time_frame[i]
                        i -= 1

                        for new_section in new_sections:
                            i += 1
                            if sorted_entity.covers(new_section): 
                                entity = sorted_entity
                            else:
                                entity = None
                            
                            time_frame.insert(i, [new_section, entity])

                i += 1


        # build requested records by combining the time frame sections and bringing them to the requested interval

        requested_records = []
        for i in range(len(time_frame)):
            entity = time_frame[i][1]
            date_time_range = time_frame[i][0]

            if time_frame[i][1] is not None:
                entity_records = entity.get_records(date_time_range.start_date_time, date_time_range.end_date_time)
                if entity.interval == interval:
                    requested_records.extend(entity_records)
                else:
                    interval_multiplier = interval // entity.interval
                    for j in range(0, len(entity_records), interval_multiplier):
                        requested_records.append(entity_records[j].compress(interval_multiplier, sort = False))

        # save requested records in database for later use
        DataEntity(interval = interval).add_records(requested_records)

        return requested_records