from .base import DownloadClient
# selenium 4
import os, time, requests
from dataclasses import dataclass
from selenium import webdriver
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as ChromiumService
from bustercp.utils.datautils import DataUtils, FileType
from bustercp.constants.constants import invalid_file_name_chars
from selenium.webdriver.chrome.options import Options


@dataclass
class FileCandidate:
    title: str
    year: int
    link: str


class OecdLibClient(DownloadClient):

    def __init__(self, base_path: str, datautils: DataUtils, username: str, password: str, user_agent: str):

        super().__init__(base_path, datautils)     

        self.username = username
        self.password = password
        self.user_agent = user_agent


    def run_download(self):
        print(f"username={self.username}, password={self.password}")

        chrome_options = Options()
        chrome_options.add_argument("--headless")

        driver = webdriver.Chrome(
            service=ChromiumService(ChromeDriverManager().install()),
            options=chrome_options
        )

        # Go to login page
        driver.get("https://www.oecd-ilibrary.org/signin?signInTarget=%2F")

        driver.find_element(By.ID, 'signname').send_keys(self.username)
        driver.find_element(By.ID, 'signpsswd').send_keys(self.password)
        driver.find_element(By.CLASS_NAME, 'c-LoginForm__submitbutton').click()
        
        time.sleep(2)

    
        s = requests.session()
        headers = {'User-Agent': self.user_agent}
        print(f'headers={headers}')
        s.headers.update(headers)

        for cookie in driver.get_cookies():
            c = {cookie['name']: cookie['value']}
            s.cookies.update(c)

        print("s=", s)

        # Go to search page, using pagesize=500 avoid clicking 'load more'
        url = "https://www.oecd-ilibrary.org/search?value1=%22AI%22&option1=dcterms_description&operator2=OR&value2=%22Artificial+intelligence%22&option2=dcterms_description&operator3=OR&value3=%22ML%22&option3=dcterms_description&operator4=OR&value4=%22Machine+learning%22&option4=dcterms_description&operator5=OR&value5=%22LLM%22&option5=dcterms_description&operator6=OR&value6=%22generative+AI%22&option6=dcterms_description&operator7=OR&value7=%22language+models%22&option7=dcterms_description&operator8=OR&value8=%22algorithmic%22&option8=dcterms_description&operator9=AND&option9=year_from&value9=2019&operator10=AND&option10=year_to&value10=&option11=pub_imprintId&value11=&option12=dcterms_language&value12=en&option15=dcterms_type&option58=contentType&value15=&option29=pub_themeId&value29=&option30=pub_countryId&value30=&sortField=default&sortDescending=true&facetOptions=51&facetNames=pub_igoId_facet&operator51=AND&option51=pub_igoId_facet&value51=%27igo%2Foecd%27&publisherId=%2Fcontent%2Figo%2Foecd&searchType=advanced&pageSize=500"
        print(f'url={url}')
        driver.get(url)


        time.sleep(2)
        
        candidates = self.create_file_candidates(driver)
        rows = driver.find_elements(By.CSS_SELECTOR, ".resultItem.table-row")

        for row in rows:
            title = row.find_element(By.CSS_SELECTOR, ".title_box .search_title a").text
            link = None
            
            try:
                link = row.find_element(By.CSS_SELECTOR, ".actions li a.action-pdf.enabled").get_attribute("href")
            except:
                print(f"skipping, title={title}")
                continue
            
            metadata = row.find_element(By.CSS_SELECTOR, ".search-metaitem.comma_separated")
            date = metadata.find_element(By.CSS_SELECTOR, "li:nth-child(1)").text
            
            year = int(date.strip()[-4:])
            candidates.append(FileCandidate(title=title, year=year, link=link))


        driver.close()

    
        for i, cand in enumerate(candidates):
            print(f"{i} Downloading {cand.title} ...")

            self.download_pdf(s, cand)




    def create_file_candidates(self, driver: any) -> list[FileCandidate]:
        candidates = []
        rows = driver.find_elements(By.CSS_SELECTOR, ".resultItem.table-row")

        for row in rows:
            title = row.find_element(By.CSS_SELECTOR, ".title_box .search_title a").text
            link = None

            if not "AI applications" in title: continue
            
            try:
                link = row.find_element(By.CSS_SELECTOR, ".actions li a.action-pdf.enabled").get_attribute("href")
            except:
                print(f"skipping, title={title}")
                continue
            
            metadata = row.find_element(By.CSS_SELECTOR, ".search-metaitem.comma_separated")
            date = metadata.find_element(By.CSS_SELECTOR, "li:nth-child(1)").text
            year = int(date.strip()[-4:])
            candidates.append(FileCandidate(title=title, year=year, link=link))

        return candidates
    

    def download_pdf(self, s:any, cand: FileCandidate):
        response = s.get(cand.link)
        response.raise_for_status()  # Will raise an HTTPError if the HTTP request returned an unsuccessful status code

        title_short = cand.title if len(cand.title) < 50 else cand.title[:50]
        for char in invalid_file_name_chars:
            title_short = title_short.replace(char, '')

        title_short = title_short.strip()

        group_path = os.path.join(self.base_path, "OECD", title_short)
        os.makedirs(group_path, exist_ok=True)

        self.datautils.write(group_path, FileType.PDF, response.content, file_name=f"{title_short}.pdf")
        self.datautils.write(group_path, FileType.YEAR, str(cand.year))
        self.datautils.write(group_path, FileType.LINK, cand.link)
        self.datautils.write(group_path, FileType.TITLE, cand.title)
