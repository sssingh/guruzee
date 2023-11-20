import os
from dotenv import load_dotenv
from dataclasses import dataclass

# load environment variables from .env (only available in dev environment)
load_dotenv()


@dataclass
class __AppConfig:
    openai_max_access_count = 200
    openai_curr_access_count = None
    mongo_client = None
    db = "mydb"
    collection = "guruzee-openai-access-counter"
    key = "current_count"
    GURUZEE_API_ENDPOINT = os.getenv("GURUZEE_API_ENDPOINT")
    HF_TOKEN = os.getenv("HF_TOKEN")
    MONGO_CONN_STR = os.getenv("MONGO_CONN_STR")
    title = "GuruZee, your go-to guru for primary school math"
    theme = "freddyaboulton/dracula_revamped"
    css = "style.css"


config = __AppConfig()
