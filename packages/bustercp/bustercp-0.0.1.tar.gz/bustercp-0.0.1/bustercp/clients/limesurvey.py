from .base import DownloadClient
import os, json, base64, requests, re, unicodedata
from dataclasses import dataclass
import urllib3
from datetime import datetime
from bustercp.utils.datautils import DataUtils, FileType

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class PdfMetadata:
    """PDF metadata."""
    country_code: str
    file_name: str
    link: str
    start_date: str
    submit_date: str



class LimeSurveyClient(DownloadClient):
    """Lime Survey client"""
    session_key = None

    def __init__(self, base_path: str, datautils: DataUtils, username: str, password: str, user_id: str,
                 survey_id: str, api_url: str, user_agent: str):
        super().__init__(base_path, datautils)      
        self.username = username
        self.password = password
        self.user_id = user_id
        self.survey_id = survey_id
        self.api_url = api_url
        self.user_agent = user_agent

        self.session_key = self.get_session_key()




    def run_download(self):
        metadata_list = self.export_responses()
        self.attact_metadata(base_path=self.base_path, metadata_list=metadata_list)

      
    def get_session_key(self):
        """Get Lime Survey session key."""
        body = {
            "method": "get_session_key",
            "params": [self.username, self.password],
            "id": self.user_id
        }
        res = requests.post(self.api_url, json=body).json()
        session_key = res['result']
        print("Session key=%s" % session_key)
        return session_key


    def export_responses(self):
        """Export responses from Lime Survey Server."""
        print("start: export_responses")
        body = {
            "method": "export_responses",
            "params": [
                self.session_key,
                self.survey_id,
                "json",
                "en",
                "full",
                "long"
            ],
            "id": self.user_id
        }

        print("selfapi_url=", self.api_url)

        res = requests.post(self.api_url, json=body).json()
        base64_string = res['result']
        base64_bytes = base64_string.encode("utf-8")
        json_str =  base64.b64decode(base64_bytes).decode("ascii")
        responses =  json.loads(json_str)['responses']
        print("responses.len=%d" % len(responses))

        metadata_list = self.responses_to_metadata_list(responses)

        count_links = 0
        for metadata in metadata_list:
            if metadata.link != None: count_links+=1
        print("count_links=", count_links)

        return metadata_list


    def responses_to_metadata_list(self, responses):
        """Convert responses to metadata list."""
        metadata_list = []
        fake_iter = 0
        for res in responses:
            for key_id in res.keys():
                for key in res[key_id].keys():
    
                    if 'link' in key and res[key_id][key] != None and 'pdf' in res[key_id][key]:
                        # if fake_iter > 5: break
                        key_file_name = key[0: len(key)-4]+'name'  
                        pdf_url = res[key_id][key]
                        pdf_file_name = res[key_id][key_file_name]
                        country_code = res[key_id]['Country']
                        start_date = res[key_id]['startdate']
                        submit_date = res[key_id]['submitdate']

                        if pdf_file_name == None or pdf_file_name == '':
                            pdf_file_name = pdf_url.rsplit('/', 1)[1].rsplit('.', 1)[0]
                         
                        pdf_file_name = self.sanitize_file(pdf_file_name)
                        metadata = PdfMetadata(country_code, pdf_file_name, pdf_url, start_date, submit_date)
                        metadata_list.append(metadata)
                        fake_iter+=1

        return metadata_list


    def attact_metadata(self, base_path, metadata_list):
        """Quick fix."""
        print("start: attact_metadata, metadata_list.len=", len(metadata_list))
        base_path = os.path.join(*base_path.split("/"))
        for md in metadata_list:
            pdf_path = os.path.join(base_path, md.country_code, md.file_name, md.file_name+".pdf")
            pdf_exists = os.path.exists(pdf_path)

            if not pdf_exists:
                self.download_file(base_path, md)


    def sanitize_file(self, value, allow_unicode=False):
        value = str(value)
        if allow_unicode:
            value = unicodedata.normalize('NFKC', value)
        else:
            value = unicodedata.normalize('NFKD', value).encode('ascii', 'ignore').decode('ascii')
        value = re.sub(r'[^\w\s-]', '', value)
        value = re.sub(r'[-\s]+', '-', value).strip('-_')
        value = value.replace('-', ' ')
        return value


    # https://stackoverflow.com/a/63198228
    def winapi_path(self, dos_path, encoding=None):
        if (not isinstance(dos_path, str) and encoding is not None): 
            dos_path = dos_path.decode(encoding)
        path = os.path.abspath(dos_path)
        if path.startswith(u"\\\\"):
            return u"\\\\?\\UNC\\" + path[2:]
        return u"\\\\?\\" + path


    def download_file(self, base_path, md: PdfMetadata):
        # pdf_path should not exceed 250 chars!, chdir
        group_name = md.file_name # md.file_name[0:70] if len(md.file_name) > 50 else md.file_name
        file_name = md.file_name # md.file_name[0:10] if len(md.file_name) > 50 else md.file_name
        group_path =  os.path.join(base_path, md.country_code, group_name)
        # print("[%s] %s" % (repr(os.path.exists(group_path)), group_path))
        pdf_path = self.winapi_path(os.path.join(group_path, file_name + ".pdf"))
        
        year = "/"

        if md.start_date != "" and md.start_date != None:
            year = str(datetime.strptime(md.start_date, "%Y-%m-%d %H:%M:%S").year)

        if not os.path.exists(pdf_path):
            try:
                print(pdf_path)
                print("md=%s" % md)
                headers = { 'User-Agent': self.user_agent }
                response = requests.get(md.link, headers=headers, allow_redirects=True, verify=False)
                
                if response.status_code >= 300:
                    raise Exception("Status code=%s" % repr(response.status_code))

                os.makedirs(group_path, exist_ok=True)
                print("waiting response...")
                # verfify=False, tmp fix: ssl.SSLCertVerificationError: certificate verify failed
                print("response=", response)


                # with open(pdf_path, "wb+") as pdf_file:
                #     pdf_file.write(response.content)
                
                # # ce ne dela daj encode(latin1).decode(utf8)
                # with open(link_path, "w+", encoding='utf8') as link_file:
                #     link_file.write(md.link)

                # with open(year_path, "w+", encoding='utf8') as year_file:
                #     year_file.write(year)

                # with open(title_path, "w+", encoding='utf8') as title_file:
                #     title_file.write(md.file_name)



                self.datautils.write(group_path, FileType.PDF, response.content, file_name=f'{file_name}.pdf')
                self.datautils.write(group_path, FileType.LINK, md.link)
                self.datautils.write(group_path, FileType.YEAR, year)
                self.datautils.write(group_path, FileType.TITLE, md.file_name)


            except Exception as ex:
                print("ex=%s" % repr(ex))

            print("\n")
