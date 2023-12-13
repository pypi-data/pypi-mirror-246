import os, csv
from datetime import datetime
from abc import ABC, abstractmethod
from bustercp.utils.utils import iso_to_country_name
from bustercp.chunkingpipelines import ChunkingPipeline, Document
from bustercp.utils.datautils import DataUtils
from  bustercp.utils.chunkingutils import write_chunks

class Chunking(ABC):


    def __init__(self, datasources_path: str, data_utils: DataUtils,
                 pipeline: ChunkingPipeline):
        self.datasources_path = datasources_path
        self.data_utils = data_utils
        self.pipeline = pipeline


    @abstractmethod
    def create_document_candidates(self, base_path: str) -> list[Document]:
        ...


    def run_chunking(self):

        unique_files = {} # key- <country_code>_<file_size>, # value-pdf_path
        datasources = os.listdir(self.datasources_path)
        was_printed = set()

        for datasource in datasources:
            print("datasource=", datasource)
            
            base_path = os.path.join(self.datasources_path, datasource, 'pdfs')
            candidates = self.create_document_candidates(base_path)

            candidates_filtered = []

            for cand in candidates:
                key2 = os.path.getsize(cand.pdf_path) if cand.pdf_path else cand.file_name
                key = f"{cand.country}_{key2}"
                value = cand.pdf_path

                if not key in unique_files:
                    unique_files[key] = value

                if value == unique_files[key]:
                    candidates_filtered.append(cand)
                else:
                    msg = f"skip duplicate={cand.pdf_path}, already found in {unique_files[key]}"

                    if not msg in was_printed:
                        print(msg)
                        was_printed.add(msg)


            print("candidates_filtered.len=%d" % len(candidates_filtered)) 


            chunks = self.pipeline.transform(candidates)

            if chunks != None and len(chunks) > 0:
                print("chunks.len=", len(chunks))
                print("chunks[0]=%s" % repr(chunks[0]))

                write_chunks(chunks, candidates, self.datasources_path, datasource)
            else:
                print(f"0 chunks created for datasource={datasource}")
