import os
from abc import ABC, abstractmethod
from dataclasses import dataclass
from bustercp.utils.datautils import DataUtils

@dataclass
class FileInfo:
    country_code: str
    link: str
    pdf_name: str
    pdf_path: str


class PdfConverter(ABC):

    def __init__(self, datasources_path: str, data_utils: DataUtils):
        self.datasources_path = datasources_path
        self.data_utils = data_utils


    @abstractmethod
    def create_file_candidates(self) -> list[FileInfo]:
        ...


    @abstractmethod
    def detect_encoding(self, pdf_path: str) -> str:
        ...


    @abstractmethod
    def convert_pdf_to_txt(self) -> str:
        ...

    
    def convert_files(self):
        
        candidates = self.create_file_candidates()

        for file_info in candidates:
            
            txt_path = file_info.pdf_path.replace(".pdf", ".txt").replace(".PDF", ".txt")
            file_text = self.process_file(file_info, txt_path)

            if(file_text != None and file_text != "" and len(file_text) > 10):

                
                with open(txt_path, 'w+', encoding='utf-8') as out_file:
                    out_file.write(file_text)


    
    def process_file(self, file_info: FileInfo, txt_path: str, overwrite=False):
        print("[%s] process_file=%s => %s" % (file_info.country_code, file_info.pdf_name, file_info.link))

        file_text = None

        if file_info.pdf_name != None:

            
        
            # if txt file not exists or is it empty
            if overwrite or not os.path.exists(txt_path) or os.path.getsize(txt_path) == 0:
                encoding = self.detect_encoding(file_info.pdf_path)
                print("       detected encoding=%s" % encoding)
                
                file_text = ""
                try:
                    file_text = self.convert_pdf_to_txt(file_info.pdf_path, codec=encoding)
                    if len(file_text) == 0: raise Exception("Empty txt file! Fix issues!")


                except Exception as ex:
                    print("Skipping corrupted pdf, ex=", ex)
            
            else:
                print("     Skipping TXT file- exists non empty txt")

        else:
            print("     Skipping file")
        
        print("\n")

        return file_text
