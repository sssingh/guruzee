import os
from dotenv import load_dotenv
from dataclasses import dataclass

# load environment variables from .env (only available in dev environment)
load_dotenv()


@dataclass
class __ServerConfig:
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
    teacher_instruction = """"""
    OPENAI_API_ENDPOINT = os.getenv("OPENAI_API_ENDPOINT")
    OPENAI_KEY = os.getenv("OPENAI_KEY")


server_config = __ServerConfig()
