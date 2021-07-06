import datetime
from abc import ABC, abstractmethod
from itertools import islice


class Validator(ABC):
    @abstractmethod
    def validate(self):
        pass


class CarsValidator(Validator):
    def __init__(self, input_file):
        self._input_file = input_file
        self._lines = self.read()
        self._format_lines()
        self._titles = self.parse_titles()
        self._data = self.parse()

    def validate(self):
        self._validate_id()
        self._validate_price()
        self._validate_volume()
        self._validate_mileage()
        self._validate_time()
        self._validate_model()

    def parse_titles(self):
        return tuple(self._lines[0].split(","))

    def read(self):
        try:
            with open(self._input_file) as file:
                lines = file.readlines()
        except FileNotFoundError:
            print("File not found")
        return lines

    def _format_lines(self):
        for index, line in enumerate(self._lines):
            self._lines[index] = line.strip("\n")

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

    def _validate_id(self):
        for index, value in enumerate(self["CAR ID"]):
            part1, part2, part3, part4, part5 = value.split("-")
            if len(part1) != 8:
                print(f"Validation error, line {index + 2} (wrong length at '{part1}')")
            if len(part2) != 4:
                print(f"Validation error, line {index + 2} (wrong length at '{part2}')")
            if len(part3) != 4:
                print(f"Validation error, line {index + 2} (wrong length at '{part3}')")
            if len(part4) != 4:
                print(f"Validation error, line {index + 2} (wrong length at '{part4}')")
            if len(part5) != 12:
                print(f"Validation error, line {index + 2} (wrong length at '{part5}')")

    def _validate_price(self):
        bought_prices = [int(price) for price in self["BOUGHT AT: PRICE"]]
        sold_prices = [int(price) for price in self["SOLD AT:PRICE"]]

        prices = zip(range(len(bought_prices)), bought_prices, sold_prices)
        for index, bought_price, sold_price in prices:
            if bought_price < 0:
                print(f"Validation error, line {index + 2} ('BOUGHT AT: PRICE' < 0)")
            if sold_price < 0:
                print(f"Validation error, line {index + 2}  ('SOLD AT:PRICE' < 0)")
            if sold_price < bought_price:
                print(f"Validation error, line {index + 2}  ('SOLD AT:PRICE' < 'BOUGHT AT: PRICE')")

    def _validate_volume(self):
        volumes = [int(volume) for volume in self["VOLUME"]]
        for index, volume in enumerate(volumes):
            if volume < 0:
                print(f"Validation error, line {index + 2}  ('VOLUME' < 0)")
            if volume == 1900 or volume == 1.9:
                print(f"Validation error, line {index + 2}  ('VOLUME' = 1900 or 1.9)")

    def _validate_mileage(self):
        mileages = [int(mileage) for mileage in self["MILEAGE"]]
        for index, mileage in enumerate(mileages):
            if mileage < 0:
                print(f"Validation error, line {index + 2}  ('MILEAGE' = 0)")
            if mileage > 250:
                print(f"Validation error, line {index + 2}  ('MILEAGE' > 250)")

    def _validate_time(self):
        bought_when_dates = [datetime.datetime.strptime(bought_when, "%d/%m/%Y")
                             for bought_when in self['BOUGHT WHEN: DATE']]
        sold_when_dates = [datetime.datetime.strptime(sold_when, "%d/%m/%Y")
                           for sold_when in self['SOLD WHEN: DATE']]

        dates = zip(range(len(bought_when_dates)), bought_when_dates, sold_when_dates)
        for index, bought_when, sold_when in dates:
            if bought_when > sold_when:
                print(f"Validation error, line {index + 2}  ('BOUGHT WHEN: DATE' > 'SOLD WHEN: DATE')")

    def _validate_model(self):
        models = [model for model in self["CAR MODEL"]]
        for index, model in enumerate(models):
            if len(model.split(",")) > 1:
                print(f"Validation error, line {index + 2}  ('CAR MODEL' has substring)")

    def __iter__(self):
        for line in self._data:
            yield line

    def __getitem__(self, item):
        for obj in self:
            for key, value in obj.items():
                if key == item:
                    yield value


if __name__ == '__main__':
    validator = CarsValidator(r"data/cars.csv")
    validator.validate()

