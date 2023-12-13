import os
from .base import Chunking
from bustercp.chunkingpipelines import Document
from bustercp.utils.datautils import FileType

class ChunkingService(Chunking):
    
    
    def create_document_candidates(self, base_path: str) -> list[Document]:
        already_printed = set()
        unique_files = {} # key- <country_code>_<file_size>, # value-pdf_path
        initial_candidates = self.create_initial_document_candidates(base_path)
        candidates = []

        for cand in initial_candidates:

            if cand.pdf_path == None or cand.pdf_path == '':
                candidates.append(cand)
            else:
                file_size = os.path.getsize(cand.pdf_path)
                key = f"{cand.country}_{file_size}"
                value = cand.pdf_path

                if not key in unique_files:
                    unique_files[key] = value

                if value == unique_files[key]:
                    candidates.append(cand)
                else:
                    msg = f"skip duplicate={cand.pdf_path}, already found in {unique_files[key]}"

                    if not msg in already_printed:
                        print(msg)
                        already_printed.add(msg)


        print("candidates.len=%d" % len(candidates)) 
        return candidates



    def create_initial_document_candidates(self, base_path: str) -> list[Document]:
        print("start: create_document_candidates")
        document_id = 0
        candidates: list[Document] = []

        for country in os.listdir(base_path):
            print("-",country)

            country_path = os.path.join(base_path, country)

            for group in os.listdir(country_path):
                print("     -", group)

                group_path = os.path.join(country_path, group)
                
                # skip empty directory
                if os.path.isdir(group_path) and not os.listdir(group_path):
                    continue

                # group_files = os.listdir(group_path)
                # pdf_idx = [i for i, file_name in enumerate(group_files) if ".pdf" in file_name.lower()][0]
                # txt_name = group_files[pdf_idx].replace(".pdf", ".txt").replace(".PDF", ".txt")
                # link_path = os.path.join(group_path, 'link.txt')
                # year_path = os.path.join(group_path, 'year.txt')
                # title_path = os.path.join(group_path, 'title.txt')
                # converted_f_path = os.path.join(group_path, txt_name)
                # pdf_path = os.path.join(group_path,  group_files[pdf_idx])

                converted_f_path = os.path.join(group_path, self.data_utils.find_converted_file_name(group_path))

                if os.path.exists(converted_f_path):
                    link = None
                    raw_text = "" 
                    year = None
                    title = None

                    if not os.path.exists(converted_f_path):
                        print("         Skipping, file was not converted from pdf to txt!")
                        continue
                    
                    raw_text = self.data_utils.read(group_path, FileType.CONV_TEXT) 
                    link = self.data_utils.read(group_path, FileType.LINK)
                    year = self.data_utils.read(group_path, FileType.YEAR)
                    title = self.data_utils.read(group_path, FileType.TITLE)
                    
                    pdf_file_name = self.data_utils.find_pdf_file_name(group_path)
                    pdf_path = ""

                    if pdf_file_name:
                        pdf_path = os.path.join(group_path, pdf_file_name)
                
                    document = Document(document_id, country, pdf_path, title, group, group, link, raw_text, year)
                    candidates.append(document)
                    document_id += 1
                else:
                    print("         Skipping...")


        return candidates
