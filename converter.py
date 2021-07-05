import argparse
from abc import ABC, abstractmethod


class Converter(ABC):
    def __init__(self):
        self._input_file = None
        self._lines = None

    @abstractmethod
    def convert(self):
        pass

    @abstractmethod
    def read(self):
        try:
            with open(self._input_file) as file:
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
    def __init__(self, input_file, output_file):
        self._input_file = input_file
        self._output_file = output_file
        self._lines = None
        self._titles = None
        self._objects = self.read()
        self._converted = self.convert()

    def convert(self):
        result_string = ""
        if len(self) > 1:
            result_string += "[ \n"
            for obj in self:
                result_string += "{ \n"
                for key, value in obj.items():
                    result_string += f'"{key}": "{value}", \n'
                result_string = result_string[0:-3] + " \n"
                result_string += "}, \n"
            result_string = result_string[0:-3] + " \n"
            result_string += "] \n"
        else:
            for obj in self:
                result_string += "{ \n"
                for key, value in obj.items():
                    result_string += f'"{key}": "{value}", \n'
                result_string = result_string[0:-3] + " \n"
                result_string += "} \n"
        return result_string

    def write(self):
        with open(self._output_file, "w") as file:
            file.write(self._converted)

    def read(self):
        super().read()
        self._titles = self.parse_titles()
        data = []
        for index, line in enumerate(self._lines):
            if index > 0:
                object_ = {}
                coll_patterns = self._find_collection_patterns(line)
                if not coll_patterns:
                    for i in range(0, len(line.split(","))):
                        try:
                            object_.update({self._titles[i]: line.split(",")[i]})
                        except IndexError:
                            print("Index out of range")
                    data.append(object_)
                else:
                    title_idx = 0
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
                            except IndexError:
                                pass
                    data.append(object_)
        return data

    def parse_titles(self):
        return tuple(self._lines[0].split(","))

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

    def __iter__(self):
        return iter(self._objects)

    def __getitem__(self, item):
        for obj in self:
            for key, value in obj.items():
                if key == item:
                    yield value

    def __len__(self):
        return len(self._objects)


def convert(input_file, output_file):
    scv_handler = SCVHandler(input_file, output_file)
    scv_handler.write()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file')
    parser.add_argument('output_file')
    input_file = parser.parse_args().input_file
    output_file = parser.parse_args().output_file
    # convert(r"data/data_file.scv", "converted.json")
    convert(input_file, output_file)
