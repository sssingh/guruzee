import requests
from server_config import server_config
from fastapi import FastAPI
from pydantic import BaseModel

guruzee = FastAPI()


class SingleImageData(BaseModel):
    data: str


def __analyze_single_image(image_data: str):
    """
    Sends the user supplied image with system instructions to GPT-4, returns the
    received response in JSON format.
    """
    image_data = {"url": f"data:image/jpeg;base64,{image_data}"}
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {server_config.OPENAI_KEY}",
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "temperature": 0.2,  # low temperature because we want deterministic responses
        "messages": [
            {"role": "system", "content": server_config.solver_persona},
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": server_config.solver_instruction},
                    {
                        "type": "image_url",
                        "image_url": image_data,
                    },
                ],
            },
        ],
        "max_tokens": 600,
    }

    response = requests.post(
        server_config.OPENAI_API_ENDPOINT, headers=headers, json=payload
    )
    return response.json()


@guruzee.post("/solve")
async def solve(image: SingleImageData):
    """
    Invokes the OpenAI API passing the raw image bytes and returns the
    response to client
    """
    output = __analyze_single_image(image.data)
    return output["choices"][0]["message"]["content"]


@guruzee.get("/health")
async def health():
    return {"Message": "Healthy and kicking!"}
