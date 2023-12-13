import os, enum


class FileType(enum.Enum):
    PDF = 0
    CONV_TEXT = 1
    CHUNK = 2
    TITLE = 3
    LINK = 4
    YEAR = 5



class DataUtils:

    def __init__(self, link_file_name: str, year_file_name: str, title_file_name: str, encoding="utf-8"):
        self.link_file_name = link_file_name
        self.year_file_name = year_file_name
        self.title_file_name = title_file_name
        self.encoding = encoding

        self.file_names = [self.link_file_name, self.year_file_name, self.title_file_name]

    
    def read(self, base_path: str, file_type: FileType):
        content = None

        if base_path == None or base_path == '':
            raise Exception("Provide valid base path")


        if file_type == FileType.PDF:
            pdf_file_name = self.find_pdf_file_name(base_path)
            content = self.read_pdf(base_path, pdf_file_name)

        elif file_type == FileType.CONV_TEXT:
            converted_text_file_name = self.find_converted_file_name(base_path)
            content = self.read_file(base_path, converted_text_file_name)
        
        elif file_type == FileType.TITLE:
            content = self.read_file(base_path, self.title_file_name)

        elif file_type == FileType.LINK:
            content = self.read_file(base_path, self.link_file_name)

        elif file_type == FileType.YEAR:
            content = self.read_file(base_path, self.year_file_name)

        else:
            raise Exception("Provide correct FileType enum")
        

        return content
    
    


    def write(self, base_path: str, file_type: FileType, content: str, file_name: str = None):

        if base_path == None or base_path == '':
            raise Exception("Provide valid base path")
        

        if file_type == FileType.PDF:
            if file_name == None or file_name == '':
                raise Exception("Provide valid file name for 'FileType.CONV_TEXT'")
             
            self.write_pdf(base_path, file_name, content)

        elif file_type == FileType.CONV_TEXT:
            if file_name == None or file_name == '':
                raise Exception("Provide valid file name for 'FileType.CONV_TEXT'")

            self.write_file(base_path, file_name, content)

        elif file_type == FileType.TITLE:
            self.write_file(base_path, self.title_file_name, content)

        elif file_type == FileType.LINK:
            self.write_file(base_path, self.link_file_name, content)

        elif file_type == FileType.YEAR:
            self.write_file(base_path, self.year_file_name, content)

        else:
            raise Exception("Provide correct FileType enum")



    
    def write_pdf(self, base_path: str, file_name: str, content: any):
        pdf_path = os.path.join(base_path, file_name)
        
        with open(pdf_path, 'wb') as f:
            f.write(content)




    def write_file(self, base_path: str, file: str, content: str):
        with open(os.path.join(base_path, file), 'w+', encoding=self.encoding) as f_out:

            content_clean = content

            if content_clean == None or content_clean == '':
                content_clean = '/'

            content_clean = content_clean.strip()

            f_out.write(content_clean)

           
    def read_file(self, base_path: str, file_name: str) -> str:
        path = os.path.join(base_path, file_name)
        content = None
        with open(path, 'r', encoding=self.encoding) as f_in:
            content = f_in.read()

        return content 
    


    def write_pdf(self, base_path: str, file: str, content: str):

        print(f"start: write_pdf, base_path={base_path}, file={file}")
        
        pdf_path = os.path.join(base_path, file)

        with open(pdf_path, 'wb') as f:
            f.write(content)



    def find_pdf_file_name(self, base_path: str):
        files = os.listdir(base_path)
        indices = [i for i, file_name in enumerate(files) if ".pdf" in file_name.lower()]
        found_file_name = None

        if len(indices) > 0 and indices[0] != -1:
            found_file_name = files[indices[0]]

        return found_file_name


    
    def find_converted_file_name(self, base_path: str):
        pdf_file_name = self.find_pdf_file_name(base_path)
        found_file_name = None

        if pdf_file_name != None:
            found_file_name = pdf_file_name.replace('.pdf', '.txt').replace('.PDF', '.txt')

        else:
            for file_name in os.listdir(base_path):
                if file_name not in self.file_names:
                    found_file_name = file_name
                    break
        
        if found_file_name == None or 'txt' not in found_file_name:
            print(f'found_file_name={found_file_name}')
            raise Exception("Converted file name not found!")

        return found_file_name
    
