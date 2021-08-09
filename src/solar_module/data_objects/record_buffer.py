from data_objects.record import Record

class RecordBuffer:

    def __init__(self, size):
        self.size = size
        self._buffer = [None] * self.size

    def add(self, record):
        if isinstance(record, Record):
            self._buffer.pop(0)
            self._buffer.append(record)
        else:
            raise TypeError("RecordBuffer only accepts Record objects")

    def top(self) -> Record:
        return self._buffer[-1]

    def bottom(self) -> Record:
        bottom_record = next((record for record in self._buffer if record is not None), None)
        return bottom_record

    def get_records(self, date_time_range):
        records = []
        for record in self._buffer:
            if record is None: continue
            if date_time_range.covers(record.recorded_time):
                records.append(record)

        return records

    @property
    def buffer(self):
        return self._buffer