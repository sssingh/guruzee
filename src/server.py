import base64
import requests
from app_config import config


# Function to encode the local image into base64 to be send over HTTP
def local_image_to_url(image_path):
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode("utf-8")
    return {"url": f"data:image/jpeg;base64,{base64_image}"}


def analyze_single_image(image_path: str, instruction: str, mode="url"):  # "local"
    if mode == "local":
        image_path = local_image_to_url(image_path)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {config.openai_api_key}",
    }
    payload = {
        "model": "gpt-4-vision-preview",
        "temperature": 0.2,
        "messages": [
            {
                "role": "system",
                "contents": """You an expert primary school maths teacher. Given an image 
             of a primary school maths problem you can analyze the problem and produce
             a detailed solution with explanation."""
                # In addition to this, given a
                # collection images from primary school maths text book you can generate
                # questions and there answers based on the topic shown in text book images,
                # you will provide the detailed answers with explanation""",
            },
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": instruction},
                    {
                        "type": "image_url",
                        "image_url": image_path,
                    },
                ],
            },
        ],
        "max_tokens": 600,
    }

    response = requests.post(config.openai_api_endpoint, headers=headers, json=payload)
    return response.json()


def solve(problem_image: str, mode="local"):
    print("P R O B L E M:\n--------------")
    display(Image(filename=problem_image))  # only in notebook
    instruction = """Analyze the 4th grade math problem in the image. Strictly first provide the answer to the problem and then only the solution explanation. 
    Put a newline after each 80 chars"""
    output = analyze_image(problem_image, instruction, mode)
    print("A N S W E R:\n------------")
    print(output["choices"][0]["message"]["content"])
    return output["choices"][0]["message"]["content"]
