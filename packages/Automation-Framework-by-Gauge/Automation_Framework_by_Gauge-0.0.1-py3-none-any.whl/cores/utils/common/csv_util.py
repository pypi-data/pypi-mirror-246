import csv
import json


class CsvUtil:

    @staticmethod
    def write_json_to_csv_file(csv_path: str, content: json):
        count: int = 0
        try:
            data_file = open(csv_path, 'w', newline='')
            csv_writer = csv.writer(data_file)
            for data in content:
                if count == 0:
                    header = data.keys()
                    csv_writer.writerow(header)
                    count += 1
                csv_writer.writerow(data.values())
        except FileNotFoundError:
            raise f'Can not found {csv_path} file'
        data_file.close()

    @staticmethod
    def convert_csv_file_to_dictionary(f_path: str, headers: list = None):
        with open(f_path, 'r') as file:
            reader = csv.DictReader(
                file, fieldnames=headers)
            return [row for row in reader]

    @staticmethod
    def write_to_csv_file(csv_path, data: list):
        with open(csv_path, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(data)
        file.close()

    @staticmethod
    def convert_csv_to_json(csv_file: str) -> [dict]:
        data = []
        with open(csv_file, 'r') as file:
            csv_data = csv.DictReader(file)
            for row in csv_data:
                data.append(row)
        return data
