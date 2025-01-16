import json
from datetime import datetime
from typing import List, Dict
from app.boundaries import FileHandlerInterface


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return super().default(obj)


class JSONFileHandler(FileHandlerInterface):
    def __init__(self, file_path: str):
        self.file_path = file_path

    def read(self) -> List[Dict]:
        try:
            with open(self.file_path, "r") as data_file:
                return json.load(data_file)
        except json.JSONDecodeError:
            raise ValueError(f"{self.file_path} contains invalid JSON.")
        except IOError as e:
            raise IOError(f"Failed to read {self.file_path}: {e}")

    def write(self, data: List[dict]) -> None:
        try:
            with open(self.file_path, "w") as file:
                # json.dump([expense.model_dump() for expense in expenses], file, indent=4, cls=DateTimeEncoder)
                json.dump(data, file, indent=4, cls=DateTimeEncoder)

        except IOError as e:
            raise IOError(f"Failed to write to {self.file_path}: {e}")