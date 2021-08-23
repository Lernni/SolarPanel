from datetime import datetime

class DateTimeRange:

    def __init__(self, start_date_time, end_date_time):
        if start_date_time > end_date_time:
            raise ValueError("Start date time is greater than end date time")
        
        self.start_date_time = start_date_time.replace(microsecond = 0)
        self.end_date_time = end_date_time.replace(microsecond = 0)

    def __str__(self):
        return "{} - {}".format(self.start_date_time, self.end_date_time)

    def __eq__(self, other):
        if isinstance(other, DateTimeRange):
            return self.start_date_time == other.start_date_time and \
                self.end_date_time == other.end_date_time
        else:
            raise TypeError("Cannot compare DateTimeRange with {}".format(type(other)))

    def toJSON(self):
        return [
            datetime.timestamp(self.start_date_time),
            datetime.timestamp(self.end_date_time)
        ]

    def covers(self, date_time):
        if isinstance(date_time, datetime):
            return self.start_date_time <= date_time <= self.end_date_time
        elif isinstance(date_time, DateTimeRange):
            return self.covers(date_time.start_date_time) and \
                self.covers(date_time.end_date_time)

    # returns, what self and other have in common
    def intersect(self, other):
        if self.start_date_time > other.end_date_time or \
            self.end_date_time < other.start_date_time:
            return None

        if self.start_date_time <= other.start_date_time:
            start_date_time = other.start_date_time
        else:
            start_date_time = self.start_date_time

        if self.end_date_time <= other.end_date_time:
            end_date_time = self.end_date_time
        else:
            end_date_time = other.end_date_time

        return DateTimeRange(start_date_time, end_date_time)


    # returns a list of DataTimeRange objects that combines self, other and their intersection 
    def split_merge(self, other, subtract = False):
        if self.start_date_time > other.end_date_time or \
            self.end_date_time < other.start_date_time:
                return [self, other]

        if self.start_date_time == other.start_date_time and \
            self.end_date_time == other.end_date_time:
                return [None] if subtract else [self]


        intersect_range = self.intersect(other)
        merge_range = self.full_merge(other)

        if merge_range.start_date_time == intersect_range.start_date_time:
            if subtract:
                return [DateTimeRange(intersect_range.end_date_time, merge_range.end_date_time)]
            else:
                return [
                    intersect_range,
                    DateTimeRange(intersect_range.end_date_time, merge_range.end_date_time)
                ]
        elif merge_range.end_date_time == intersect_range.end_date_time:
            if subtract:
                return [DateTimeRange(merge_range.start_date_time, intersect_range.start_date_time)]
            else:
                return [
                    DateTimeRange(merge_range.start_date_time, intersect_range.start_date_time),
                    intersect_range
                ]
        else:
            if subtract:
                return [
                    DateTimeRange(merge_range.start_date_time, intersect_range.start_date_time),
                    DateTimeRange(intersect_range.end_date_time, merge_range.end_date_time)
                ]
            else:
                return [
                    DateTimeRange(merge_range.start_date_time, intersect_range.start_date_time),
                    intersect_range,
                    DateTimeRange(intersect_range.end_date_time, merge_range.end_date_time)
                ]

    # returns a new DateTimeRange that is the union of self and other
    def full_merge(self, other):
        if self.start_date_time <= other.start_date_time and \
            self.end_date_time <= other.end_date_time:
                return DateTimeRange(self.start_date_time, other.end_date_time)
        elif self.start_date_time > other.start_date_time and \
            self.end_date_time > other.end_date_time:
                return DateTimeRange(other.start_date_time, self.end_date_time)
        elif self.start_date_time > other.start_date_time and \
            self.end_date_time <= other.end_date_time:
                return DateTimeRange(other.start_date_time, other.end_date_time)
        else: return DateTimeRange(self.start_date_time, self.end_date_time)