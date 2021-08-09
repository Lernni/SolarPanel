import logging

from data_access.globals import DB_PATH
from data_access.data_entity import DataEntity
from data_objects.date_time_range import DateTimeRange

class DatabaseHandler:

    entities = []
    current_entity_index = None
    RECORD_LIMIT = 40

    def init():

        # check folder structure
        DB_PATH.mkdir(parents = True, exist_ok = True)

        # list of all csv files in folder
        csv_files = [f.name for f in DB_PATH.iterdir() if f.suffix == '.csv']

        # analyze and check database
        for csv_file in csv_files:
            try:
                DatabaseHandler.entities.append(DataEntity(csv_file))
            except ValueError as e:
                logging.info("found corrupted db entity '" + csv_file + "' Error: " + e.args[0])


    def add_entity(entity) -> int:
        DatabaseHandler.entities.append(entity)
        return len(DatabaseHandler.entities) - 1


    def add_records(records) -> bool:
        if len(records) == 0:
            return True

        # check interval
        # if interval is 1 -> continuous saving
        
        if records[0].interval == 1:
            if DatabaseHandler.current_entity_index is None:
                DatabaseHandler.current_entity_index = DatabaseHandler.add_entity(DataEntity())

            if DatabaseHandler.entities[DatabaseHandler.current_entity_index].record_count == DatabaseHandler.RECORD_LIMIT:
                DatabaseHandler.current_entity_index = DatabaseHandler.add_entity(DataEntity())

            current_entity = DatabaseHandler.entities[DatabaseHandler.current_entity_index]

            logging.info(str(current_entity.record_count) + " + " + str(len(records))) 
            if current_entity.record_count + len(records) <= DatabaseHandler.RECORD_LIMIT:
                return current_entity.add_records(records)
            else:
                place_remaining = DatabaseHandler.RECORD_LIMIT - current_entity.record_count
                current_entity.add_records(records[:place_remaining])
                records = records[place_remaining:]
                return DatabaseHandler.add_records(records)

        else:

            # if interval is greater than 1
            # -> check if time span and interval already exists in database
            # -> if not, create new entity and add records

            for entity in DatabaseHandler.entities:
                if entity.interval != records[0].interval: continue

                record_range = DateTimeRange(records[0].recorded_time, records[-1].recorded_time)
                if entity.range.intersect(record_range) is None: continue

                # range already exists
                if entity.range.covers(record_range): return True

                # range exists partially
                remaining_range = entity.range.split_merge(record_range, subtract = True)[0]
                new_records = [record for record in records if remaining_range.covers(record.recorded_time)]
                return DatabaseHandler.add_records(new_records)

            # range does not exist -> create new entity and add records
            new_entity = DataEntity().add_records(records)
            DatabaseHandler.add_entity(new_entity)
            return True
        

    def get_records(date_time_range, interval = 1):
        time_frame = [
            [date_time_range, None]
        ]

        end_date_time = date_time_range.end_date_time
        start_date_time = date_time_range.start_date_time

        # find entities that have data in the requested time frame
        # try to include entities that have an interval divisible by the requested interval
        # this minimizies load when compromising records to the given interval

        divider_intervals = ((interval % 2) == 0)

        # sort entities by interval
        # entities with the highest interval will be processed first
        # entities that have a lower interval and cover the same time frame as a higher interval entity will be ignored

        sorted_entitites = sorted(DatabaseHandler.entities, key = lambda e: e.interval)

        for sorted_entity in sorted_entitites:
            if sorted_entity.range.start_date_time > end_date_time or \
                sorted_entity.range.end_date_time < start_date_time or \
                sorted_entity.interval > interval: continue

            if divider_intervals:
                if ((interval % sorted_entity.interval) != 0): continue
            else:
                if (interval != sorted_entity.interval): continue

            # loop through already applied entities to see if the current entity can be applied to cover gaps in the requested time frame
            # if a gap is found, apply the entity to fill the gap
            
            i = 0
            while i < len(time_frame):
                if time_frame[i][1] is None:
                    fillable_section = time_frame[i][0].intersect(sorted_entity.range)
                    if fillable_section is not None:
                        new_sections = time_frame[i][0].split_merge(sorted_entity.range)

                        del time_frame[i]
                        i -= 1

                        for new_section in new_sections:
                            i += 1
                            if fillable_section == new_section:
                                entity = sorted_entity
                            else:
                                entity = None
                            
                            time_frame.insert(i, [new_section, entity])

                i += 1


        # build requested records by combining the time frame sections and bringing them to the requested interval

        requested_records = []
        for i in range(0, len(time_frame)):
            entity = time_frame[i][1]
            date_time_range = time_frame[i][0]

            if time_frame[i][1] is not None:
                entity_records = entity.get_records(date_time_range)
                if entity.interval == interval:
                    requested_records.extend(entity_records)
                else:
                    interval_multiplier = interval // entity.interval
                    for j in range(0, len(entity_records), interval_multiplier):
                        requested_records.append(entity_records[j].compress(interval_multiplier, sort = False))

        # save requested records in database for later use
        if len(requested_records) > 0 and interval != 1:
            DataEntity(interval).add_records(requested_records)

        return requested_records