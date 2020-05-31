
import datetime
import logging
import os
from typing import List

from consts import local_data_path
from models import DataSet, FetchedFile

class FetchedFileIO:
    def write(self, fetched_file: FetchedFile, content: bytes) -> bool:
        with open(self._fetched_file_path(fetched_file), "wb") as htmlFile:
            try:
                htmlFile.write(content)
            except Exception as e:
                logging.error(f"Could not write {fetched_file.name}", e)
                return False
        logging.info(f"Successfully wrote fetched file {fetched_file.name}")
        return True

    def read(self, fetched_file: FetchedFile) -> bytes:
        content = None
        try:
            with open(self._fetched_file_path(fetched_file), "r") as htmlFile:
                content = htmlFile.read()
                logging.info(f"Successfully read fetched file {fetched_file.name}")
        except Exception as e:
            logging.error(f"Could not read {fetched_file.name}", e)
        return content

    def all(self) -> List[FetchedFile]:
        return [
            fetched_file for fetched_file in 
            [
                FetchedFile.from_file_name(filename)
                for filename in os.listdir(local_data_path)
            ]
            if fetched_file
        ]
    def _fetched_file_path(self, fetched_file: FetchedFile) -> str:
        return os.path.join(
            local_data_path,
            fetched_file.name
        )
