from dataclasses import dataclass


@dataclass
class __AppConfig:
    openai_api_endpoint = "https://api.openai.com/v1/chat/completions"
    openai_api_key = ""


config = __AppConfig()
