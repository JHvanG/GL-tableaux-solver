from pathlib import Path
import csv
import os


class DataHandler(object):
    def __init__(self):
        self.storage_path = os.path.join(Path(__file__).parents[1], "data")

    def write_memory_data(self, content):
        if not os.path.exists(self.storage_path + "\memory_data.csv"):
            with open(self.storage_path + '\memory_data.csv', mode='w', newline='\n') as file:
                data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                data_writer.writerow(["length", "memory"])
                data_writer.writerow(content)
        else:
            with open(self.storage_path + '\memory_data.csv', mode='a', newline='\n') as file:
                data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                data_writer.writerow(content)

    def write_time_data(self, content):
        if not os.path.exists(self.storage_path + "\\time_data.csv"):
            with open(self.storage_path + '\\time_data.csv', mode='w', newline='\n') as file:
                data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                data_writer.writerow(["length", "memory"])
                data_writer.writerow(content)
        else:
            with open(self.storage_path + '\\time_data.csv', mode='a', newline='\n') as file:
                data_writer = csv.writer(file, delimiter=',', quotechar='"', quoting=csv.QUOTE_NONNUMERIC)
                data_writer.writerow(content)
