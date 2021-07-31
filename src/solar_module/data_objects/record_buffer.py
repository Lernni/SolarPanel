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
        return self._buffer[0]

    def get_records(self, start_time, end_time):
        return [m for m in self._buffer if start_time <= m.recorded_time <= end_time]

    @property
    def buffer(self):
        return self._buffer