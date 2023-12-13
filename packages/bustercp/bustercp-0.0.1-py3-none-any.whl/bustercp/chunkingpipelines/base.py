from abc import ABC, abstractmethod
from dataclasses import dataclass
from bustercp.utils.datautils import DataUtils

@dataclass
class Document:
    id: int
    country: str
    pdf_path: str
    title: str
    group: str
    file_name: str
    link: str
    text: str
    year:int


@dataclass
class Chunk:
    doc_id: int
    p_id: int
    text: str


class ChunkingPipeline(ABC):


    def __init__(self, chunk_max_length: int, data_utils: DataUtils):
        self.chunk_max_length = chunk_max_length
        self.data_utils = data_utils

    @abstractmethod
    def transform(self, documents: list[Document]) -> list[Chunk]:
        ...
