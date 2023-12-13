from bustercp.pdfconverters import PdfConverterService
from bustercp.chunking import ChunkingService
from bustercp.clients import LimeSurveyClient, OecdLibClient, CatalogueToolsClient
from bustercp.chunkingpipelines import ChunkingPipelineBeta
from bustercp.utils.datautils import DataUtils

if __name__ == "__main__":
    
    print("start: __main__")

    DATASOURCES_PATH = "./data"
    CHUNK_MAX_LENGTH = 1000
    OECDLIB_BASE_PATH="./data/OECDLib/pdfs"
    OECDLIB_USERNAME="oecd-sti2023"
    OECDLIB_PASSWORD="oecdilibrary2023"
    OECDLIB_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0"
  
    LIMESURVEY_BASE_PATH="./data/LimeSurvey v2/pdfs"
    LIMESURVEY_USERNAME="jan.sturm"
    LIMESURVEY_PASSWORD="oecdlimesurvey2023"
    LIMESURVEY_USER_ID=24
    LIMESURVEY_SURVEY_ID=202102
    LIMESURVEY_API_URL="https://ai.stipsurvey.org/admin/remotecontrol/index.php?r=plugins/unsecure&plugin=AuthRemoteToken"
    LIMESURVEY_USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/120.0"

    CATALOGUE_TOOLS_BASE_PATH="./data/OECD Catalogue of Tools/pdfs"


    LINK_FILE_NAME = "link.txt"
    YEAR_FILE_NAME = "year.txt"
    TITLE_FILE_NAME = "title.txt"


    datautils = DataUtils(
        link_file_name=LINK_FILE_NAME,
        year_file_name=YEAR_FILE_NAME,
        title_file_name=TITLE_FILE_NAME,
    )


    limesurvey = LimeSurveyClient(
        base_path=LIMESURVEY_BASE_PATH,
        datautils=datautils,
        username=LIMESURVEY_USERNAME,
        password=LIMESURVEY_PASSWORD,
        user_id=LIMESURVEY_USER_ID,
        survey_id=LIMESURVEY_SURVEY_ID,
        api_url=LIMESURVEY_API_URL,
        user_agent=LIMESURVEY_USER_AGENT,
    )

    limesurvey.run_download()


    oecdlib = OecdLibClient(
        base_path=OECDLIB_BASE_PATH,
        datautils=datautils,
        username=OECDLIB_USERNAME,
        password=OECDLIB_PASSWORD,
        user_agent=OECDLIB_USER_AGENT,
    )
    oecdlib.run_download()

    cataloguetools = CatalogueToolsClient(
        base_path=CATALOGUE_TOOLS_BASE_PATH,
        datautils=datautils,
    )
    cataloguetools.run_download()


    converter = PdfConverterService(
        datasources_path=DATASOURCES_PATH,
        data_utils=datautils,
    )
    converter.convert_files()
    

    chunking_pipeline = ChunkingPipelineBeta(
        chunk_max_length=CHUNK_MAX_LENGTH,
        data_utils=datautils,
    )

    chunking = ChunkingService(
        datasources_path=DATASOURCES_PATH,
        data_utils=datautils,
        pipeline=chunking_pipeline,
    )

    chunking.run_chunking()
