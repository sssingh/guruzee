import os
from dotenv import load_dotenv
from dataclasses import dataclass

# load environment variables from .env (only available in dev environment)
load_dotenv()


@dataclass
class __AppConfig:
    solver_persona = """You an expert primary school maths teacher. Given an 
            image of a primary school maths problem you can analyze the problem and 
            produce a detailed solution with explanation."""
    teacher_persona = (
        solver_persona
        + """ \nIn addition to this, given a
            collection images from primary school maths text book you can generate
            questions and there answers based on the topic shown in text book images,
            you will provide the detailed answers with explanation"""
    )
    solver_instruction = """Analyze the primary school math problem in the the image. 
            Strictly first provide the answer to the problem and then only the solution 
            explanation. Put a newline after each 80 chars"""
    openai_max_access_count = 200
    openai_curr_access_count = None
    mongo_client = None
    db = "mydb"
    collection = "guruzee-openai-access-counter"
    key = "current_count"
    OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
    GURUZEE_API_ENDPOINT = os.getenv("GURUZEE_API_ENDPOINT")
    OPENAI_KEY = os.getenv("OPENAI_KEY")
    HF_TOKEN = os.getenv("HF_TOKEN")
    MONGO_CONN_STR = os.getenv("MONGO_CONN_STR")
    title = "GuruZee, your go-to guru for primary school math"
    theme = "freddyaboulton/dracula_revamped"
    css = "style.css"


config = __AppConfig()
