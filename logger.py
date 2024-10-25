class Logger:
    def __init__(self):
        self._fields = {}

    @property
    def fields(self):
        return self._fields