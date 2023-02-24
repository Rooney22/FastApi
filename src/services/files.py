import csv
from io import StringIO
from datetime import datetime
from typing import BinaryIO, List
from src.models.operation import Operation

class FilesService:
    @staticmethod
    def upload(file: BinaryIO):
        reader = csv.DictReader((line.decode() for line in file))
        for row in reader:
            print(row)

    @staticmethod
    def download_report(operations: List[Operation]):
        output = StringIO()
        data = []
        for operation in operations:
            data.append({
                'id': operation.id,
                'mass': operation.mass,
                'date_start': operation.date_start,
                'date_end': operation.date_end,
                'tank_id': int,
                'product_id': int,
                'created_at': datetime,
                'created_by': int,
                'modified_at': datetime,
                'modified_by': int,
            })
        writer = csv.DictWriter(output, fieldnames=data[0].keys())
        writer.writeheader()
        for obj in data:
            writer.writerow(obj)
        output.seek(0)
        return output
