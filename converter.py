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
        self._objects = self.read()

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
                coll_patterns = self.find_collect_patterns(line)
                if not coll_patterns:
                    for i in range(0, len(line.split(","))):
                        try:
                            object_.update({self._titles[i]: line.split(",")[i]})
                        except IndexError:
                            print("Index out of range")
                    data.append(object_)
                else:
                    title_idx = 0
                    zeroing = True
                    for part in line.split('"'):
                        value_idx = 0
                        if part not in coll_patterns:
                            for value in part.split(","):
                                if value.replace(" ", "") != "":
                                    try:
                                        if part.split(",")[value_idx] != '':
                                            object_.update({self._titles[title_idx]: part.split(",")[value_idx]})
                                            value_idx += 1
                                            title_idx += 1
                                        else:
                                            object_.update({self._titles[title_idx]: part.split(",")[value_idx + 1]})
                                            value_idx += 1
                                            title_idx += 1
                                    except IndexError:
                                        pass
                        else:
                            try:
                                object_.update({self._titles[title_idx]: part})
                                value_idx += 1
                                title_idx += 1
                                zeroing = False
                            except IndexError:
                                pass
                    data.append(object_)
        return data

    def parse_titles(self):
        return tuple(self._lines[0].split(","))

    @staticmethod
    def find_collect_patterns(line):
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

    def __iter__(self):
        return iter(self._objects)


if __name__ == '__main__':
    scv_handler = SCVHandler(r"data/data_file.scv")
    for i in scv_handler:
        print(i)