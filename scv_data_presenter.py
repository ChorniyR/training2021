class CSVDataPresenter:
    def __init__(self, data, titles):
        self._titles = None
        self._data = data

    @property
    def titles(self):
        return self._titles

    @property
    def data(self):
        return self._data

    def __iter__(self):
        for line in self._data:
            yield line

    def __getitem__(self, item):
        for obj in self:
            for key, value in obj.items():
                if key == item:
                    yield value
