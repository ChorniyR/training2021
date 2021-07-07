from itertools import islice
from scv_data_presenter import CSVDataPresenter

class CSVDataReader():
    def __init__(self, input_file):
        self._input_file = input_file
        self._lines = self.read()
        self._format_lines()
        self._titles = self.parse_titles()
        self._data = self.parse()

    def parse_titles(self):
        return tuple(self._lines[0].split(","))

    def _format_lines(self):
        for index, line in enumerate(self._lines):
            self._lines[index] = line.strip("\n")

    def read(self):
        try:
            with open(self._input_file) as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File not found")
        return lines

    def parse(self):
        self.read()
        self._titles = self.parse_titles()
        data = []
        for index, line in enumerate(islice(self._lines, 1, None)):
            object_ = {}
            coll_patterns = self._find_collection_patterns(line)

            titles = list(self._titles)
            for part in line.split('"'):
                if part not in coll_patterns:
                    for value in part.split(","):
                        if value.replace(" ", "") != "":
                            try:
                                if value != '':
                                    object_.update({titles[0]: value})
                                    titles.remove(titles[0])
                                else:
                                    object_.update({titles[0]: value})
                                    titles.remove(titles[0])
                            except IndexError:
                                pass
                else:
                    try:
                        object_.update({titles[0]: part})
                        titles.remove(titles[0])
                    except IndexError:
                        pass
            data.append(object_)
        return data

    @staticmethod
    def _find_collection_patterns(line):
        patterns = []
        pattern = ""
        opened = False
        for symb in line:
            if opened:
                pattern += symb

            if symb == '"':
                if opened:
                    opened = False
                    patterns.append(pattern.replace('"', ''))
                    pattern = ""
                elif not opened:
                    opened = True
        return patterns

    @property
    def data(self):
        return self._data

    def get_data_presenter(self):
        return CSVDataPresenter(self._data, self._titles)

if __name__ == '__main__':
    reader = CSVDataReader(r"data/cars.csv")
    presenter = reader.get_data_presenter()
    for data in presenter:
        print(data)