import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bustercp.utils.datautils import DataUtils

class DownloadClient(ABC):

    def __init__(self, base_path: str, datautils: DataUtils):
        self.base_path = base_path
        self.datautils = datautils

        # avoid exceptions related to base_path not exists...
        os.makedirs(base_path, exist_ok=True)


    @abstractmethod
    def run_download(self):
        ...
