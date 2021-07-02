import random
import re
import string
from abc import ABC, abstractmethod


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
                self._format_lines()
        except FileNotFoundError:
            print("File not found")
            pass

    @abstractmethod
    def write(self):
        pass

    def _format_lines(self):
        for index, line in enumerate(self._lines):
            self._lines[index] = line.strip("\n")


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
        self._data = self.read()

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
                object_ = {}
                coll_patterns = self._find_collect_patterns(line)
                if not coll_patterns:
                    for i in range(0, len(line.split(","))):
                        try:
                            object_.update({self._titles[i]: line.split(",")[i]})
                        except IndexError:
                            print("Index out of range")
                    data.append(object_)
                else:
                    i = 0
                    for part in line.split('"'):
                        if part not in coll_patterns:
                            for p in part.split(","):
                                if p != "":
                                    try:
                                        object_.update({self._titles[i]: part.split(",")[i]})
                                        i += 1
                                    except IndexError:
                                        pass
                        else:
                            try:
                                object_.update({self._titles[i]: part})
                                i += 1
                            except IndexError:
                                pass
                    data.append(object_)
        return data

    def parse_titles(self):
        return tuple(self._lines[0].split(","))

    @staticmethod
    def _find_collect_patterns(line):
        separator = "qwe"
        new_line = line.replace('""', '"').replace('""', separator)
        try:
            str_patterns = re.search(r"qwe(.*)qwe", new_line).group().strip(separator)
            return str_patterns
        except AttributeError:
            new_lines = line.replace('"', separator)
            str_patterns = re.findall(r'qwe(.*)qwe', new_lines)
            return str_patterns

    def __iter__(self):
        return iter(self._data)


if __name__ == '__main__':
    scv_handler = SCVHandler(r".\data\data_file.scv")
    for i in scv_handler:
        print(i)
