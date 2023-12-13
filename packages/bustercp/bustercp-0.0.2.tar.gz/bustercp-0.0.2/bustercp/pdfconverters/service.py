import os, io, re, chardet
from .base import PdfConverter, FileInfo
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from bustercp.utils.datautils import FileType

class PdfConverterService(PdfConverter):



    def create_file_candidates(self) -> list[FileInfo]:
        """
        Create file candidates for conversion from pdf to txt, based on provided datasources path.
        Path './data' would correspond to hiearhy:
        - data:
            - Datasource1
            - Datasource2
            - Datasource3
        """
        datasources = os.listdir(self.datasources_path)

        file_candidates = []

        for datasource in datasources:
            print("##############################")
            print("datasource=%s" % datasource)
            print("##############################")
            base_path = os.path.join(self.datasources_path, datasource, "pdfs")
            countries = os.listdir(base_path)

            for country in countries:
                print("     -%s" % (country))

                country_path = os.path.join(base_path, country)
                groups = os.listdir(country_path)

                for group in groups:
                    print("         -%s" % (group))

                    group_path = os.path.join(country_path, group)

                    print(f'group_path={group_path}')

                    files = os.listdir(group_path)
                    pdf_idx = self.find_pdf_idx(files)

                    if pdf_idx == -1:
                        # raise Exception("No pdf file found!")
                        continue

                    pdf_name = self.data_utils.find_pdf_file_name(group_path)
                    print(f'group_path={group_path}')
                    print(f'pdf_name={pdf_name}')
                    pdf_path = os.path.join(group_path, pdf_name)
                    link = self.data_utils.read(group_path, FileType.LINK)
                    
                    file_candidates.append(FileInfo(country, link, pdf_name, pdf_path))
            print("\n")

        return file_candidates
    


    def find_pdf_idx(self, files: list[str]):
        """
        Find index of pdf file in list of file names
        """
        idx = -1
        for i, file in enumerate(files):
            if ".pdf" in file.lower():
                idx = i
                break
        return idx
    

    # https://stackoverflow.com/a/63198228
    def winapi_path(self, dos_path, encoding=None):
        """
        Quick fix for long paths on windows- not linux compatible. TODO for linux!
        """

        print("dos_path=", dos_path)
        if (not isinstance(dos_path, str) and encoding is not None): 
            dos_path = dos_path.decode(encoding)
        path = os.path.abspath(dos_path)
        if path.startswith(u"\\\\"):
            return u"\\\\?\\UNC\\" + path[2:]
        return u"\\\\?\\" + path



    def convert_pdf_to_txt(self, file_path, codec):
        """
        Read pdf file and convert it txt file with same name as pdf file
        """
        rsrcmgr = PDFResourceManager()
        retstr = io.StringIO()
        converter = TextConverter(rsrcmgr, retstr, laparams=LAParams(), codec=codec)
        page_interpreter = PDFPageInterpreter(rsrcmgr, converter)

        text_filtered = ''

        with open(file_path, 'rb') as fh:
            
            for page_number, page in enumerate(PDFPage.get_pages(fh, caching=False, check_extractable=True)):
                try:
                    # print("page=", page_number)
                    page_interpreter.process_page(page)
                    text = retstr.getvalue()

                    if ('..........' in text) \
                        or ( re.match('table of contents',text,re.IGNORECASE) != None) \
                        or (page_number < 10 and re.match('(?<![a-zA-z])contents',text,re.IGNORECASE) != None):
                        pass
                    else:
                        text_filtered += text

                except Exception as ex:
                    print("Skipping PAGE=", page_number, "err=", ex)

                retstr.truncate(0)
                retstr.seek(0)

        converter.close()
        return text_filtered


    def detect_encoding(self, pdf_path: str) -> str:
        encoding = ''

        with open(pdf_path, 'rb') as pdf_file:
            # Read the first few bytes of the file to use for encoding detection
            sample = pdf_file.read(1024)

            # Detect the encoding of the sample bytes using chardet
            result = chardet.detect(sample)

            if result['encoding'] != None: encoding = result['encoding']

        return encoding
