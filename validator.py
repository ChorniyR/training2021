import argparse
import datetime
import logging
import re
from abc import ABC, abstractmethod

from csv_data_reader import CSVDataReader

logging.basicConfig(filename="errors.log", level=logging.INFO)


class Validator(ABC):
    @abstractmethod
    def validate(self):
        pass


class CarsValidator(Validator):
    def __init__(self, presenter):
        self._presenter = presenter

    def validate(self):
        logging.info(f"start logging at {datetime.datetime.now()}")

        self._validate_id()
        self._validate_price()
        self._validate_volume()
        self._validate_mileage()
        self._validate_time()
        self._validate_model()

    def _validate_id(self):
        pattern = r"[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}"
        for index, value in enumerate(self._presenter["CAR ID"]):
            if re.match(pattern, value) is None:
                logging.info(f"Validation error, line {index + 2}, invalid uuid")

    def _validate_price(self):
        bought_prices = [int(price) for price in self._presenter["BOUGHT AT: PRICE"]]
        sold_prices = [int(price) for price in self._presenter["SOLD AT:PRICE"]]

        prices = zip(range(len(bought_prices)), bought_prices, sold_prices)
        for index, bought_price, sold_price in prices:
            if bought_price < 0:
                logging.info(f"Validation error, line {index + 2}, 'BOUGHT AT: PRICE' < 0")
            if sold_price < 0:
                logging.info(f"Validation error, line {index + 2}, 'SOLD AT:PRICE' < 0")
            if sold_price < bought_price:
                logging.info(f"Validation error, line {index + 2}, 'SOLD AT:PRICE' < 'BOUGHT AT: PRICE'")

    def _validate_volume(self):
        volumes = [int(volume) for volume in self._presenter["VOLUME"]]
        for index, volume in enumerate(volumes):
            if volume < 0:
                logging.info(f"Validation error, line {index + 2}, 'VOLUME' < 0")
            if volume == 1900 or volume == 1.9:
                logging.info(f"Validation error, line {index + 2}, 'VOLUME' = 1900 or 1.9")

    def _validate_mileage(self):
        mileages = [int(mileage) for mileage in self._presenter["MILEAGE"]]
        for index, mileage in enumerate(mileages):
            if mileage < 0:
                logging.info(f"Validation error, line {index + 2}, 'MILEAGE' = 0")
            if mileage > 250:
                logging.info(f"Validation error, line {index + 2}, 'MILEAGE' > 250")

    def _validate_time(self):
        bought_when_dates = [datetime.datetime.strptime(bought_when, "%d/%m/%Y")
                             for bought_when in self._presenter['BOUGHT WHEN: DATE']]
        sold_when_dates = [datetime.datetime.strptime(sold_when, "%d/%m/%Y")
                           for sold_when in self._presenter['SOLD WHEN: DATE']]

        dates = zip(range(len(bought_when_dates)), bought_when_dates, sold_when_dates)
        for index, bought_when, sold_when in dates:
            if bought_when > sold_when:
                logging.info(f"Validation error, line {index + 2}, 'BOUGHT WHEN: DATE' > 'SOLD WHEN: DATE'")

    def _validate_model(self):
        models = [model for model in self._presenter["CAR MODEL"]]
        for index, model in enumerate(models):
            if len(model.split(",")) > 1:
                logging.info(f"Validation error, line {index + 2}, 'CAR MODEL' has a substring")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('input_file', help="path to *.csv file")
    input_file = parser.parse_args().input_file

    reader = CSVDataReader(input_file)
    presenter = reader.get_data_presenter()
    validator = CarsValidator(presenter)
    validator.validate()
