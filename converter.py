from abc import ABC, abstractmethod
from itertools import product


class Converter(ABC):
    def __init__(self):
        self._path = None
        self._lines = None

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def read(self):
        try:
            with open(self._path) as file:
                self._lines = file.readlines()
        except FileNotFoundError:
            print("File not found")
            pass

    @abstractmethod
    def write(self):
        pass


class JSONHandler(Converter):
    def __init__(self, path):
        self._path = path
        self._lines = None

    def write(self):
        try:
            with open(self._path) as file:
                pass
        except FileExistsError:
            pass

    def read(self):
        pass

    def convert(self):
        pass


class SCVHandler(Converter):
    def __init__(self, path):
        self._path = path
        self._lines = None
        self._titles = None

    def get_as_dict(self):
        pass

    def convert(self):
        pass

    def write(self):
        pass

    def read(self):
        super().read()
        self._titles = self.parse_titles()
        data = []
        for index, line in enumerate(self._lines):
            if index > 0:
                # pairs = [{title: cell} for cell in line.split(",") for title in self._titles]
                object_ = {}
                for i in range(0, len(line.split(","))):
                    try:
                        object_.update({self._titles[i]: line.split(",")[i]})
                    except IndexError:
                        print("Index out of range")
                        pass
                data.append(object_)
        return data

    def parse_titles(self):
        return tuple(self._lines[0].split(","))


if __name__ == '__main__':
    scv_handler = SCVHandler(".\data\data_file.scv")
    for obj in scv_handler.read():
        print(obj)
