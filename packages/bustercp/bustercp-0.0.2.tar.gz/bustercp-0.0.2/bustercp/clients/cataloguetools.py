from .base import DownloadClient
import json, os, re, requests
from bs4 import BeautifulSoup
from datetime import datetime
from bustercp.utils.utils import country_name_to_iso
from bustercp.utils.datautils import FileType
from bustercp.constants.constants import invalid_file_name_chars

class CatalogueToolsClient(DownloadClient):

    # source	country	title	doc_id	p_id	content	link	year
    def run_download(self):

        url = "https://oecd-ai.case-api.buddyweb.fr/tools"
        lastPage = int(json.loads(requests.get(url).content)['lastPage'])
        print(f'lastPage={lastPage}')

        curr_page = 1
        text_chunks = []
        titles = []
        years = []
        links = []
        countries = []

        while(curr_page <= lastPage):
            print(curr_page)

            curr_url = f'https://oecd-ai.case-api.buddyweb.fr/tools?page={curr_page}'

            res = json.loads(requests.get(curr_url).content)

            for d in res['data']:
                text_chunk, title, year, link, country = self.create_chunk(d)
                text_chunks.append(text_chunk)
                titles.append(title)
                years.append(year)
                links.append(link)
                countries.append(country)

            curr_page += 1

        

        for i, (text_chunk, title, year, link, country) in enumerate(zip(text_chunks, titles, years, links, countries)):

            # chunk = [datasource, country, title, doc_id, p_id, text_chunk, link, year]

            title_short = title if len(title) < 50 else title[:50]
            for char in invalid_file_name_chars:
                title_short = title_short.replace(char, '')

            title_short = title_short.strip()
            
            country_code = country_name_to_iso(country)

            if country_code == None:
                country_code = "unknown"

            country_path = os.path.join(self.base_path, country_code)
            os.makedirs(country_path, exist_ok=True)
            
            group_path = os.path.join(country_path, title_short)
            os.makedirs(group_path, exist_ok=True)

            self.datautils.write(group_path, FileType.LINK, link)
            self.datautils.write(group_path, FileType.TITLE, title)
            self.datautils.write(group_path, FileType.YEAR, year)
            
            self.datautils.write(group_path, FileType.CONV_TEXT, text_chunk, file_name=f'{title_short}.txt')


    def clean_html(self, html_content) -> str:
        soup = BeautifulSoup(html_content,  "html.parser")

        for script in soup(["script", "style"]):  # Remove script and style elements
            script.extract()
        return " ".join(soup.stripped_strings)  # Get text and join together


    def extract_year(date_str):
        # Parse the date string
        dt = datetime.strptime(date_str, "%Y-%m-%dT%H:%M:%S.%fZ")
        
        # Return the year
        return dt.year


    def create_chunk(self, d:any):
        name = d['name']
        slug = d['slug']
        excerpt = d['excerpt']
        content = d['content']
        publishedAt = d['publishedAt']
        githubStars = d['githubStars']
        githubForks = d['githubForks']
        link = d['websiteLink']
        status = d['status']
        createdAt = d['createdAt']
        objectives = ",".join(obj['name'] for obj in d['objectives'])
        country = "/"

        if len(d["countries"]) > 0:
            country = d["countries"][0]["name"]

        text = f'''
        In OECD Catalogue of Tools is tool with:
        Name: {name}.
        Slug: {slug}.
        Excerpt: {excerpt}.
        Content: {content}.
        PublishedAt: {publishedAt}.
        GithubStars: {githubStars}.
        GithubForks: {githubForks}.
        Status: {status}.
        CreatedAt: {createdAt}.
        Objectives: {objectives}.
        '''

        text = self.clean_html(text)
        text = text.replace('\t', ' ')
        text = text.replace('|', ', ')
        text = re.sub('\ +', ' ', text)
        text = text.replace('\n  ', '\n')
        text = text.replace('\n', ' ')
        text = text.strip()

        title = name
        year = None

        try:
            year = self.extract_year(publishedAt)
        except:
            year = "/"
        return text, title, year, link, country
