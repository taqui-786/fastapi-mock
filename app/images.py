from dotenv import load_dotenv
from imagekitio import ImageKit
import os
import requests, base64

load_dotenv()

imagekit = ImageKit(
    private_key=os.environ.get("IMAGEKIT_PRIVATE_KEY"),
    # public_key=os.environ.get("IMAGEKIT_PUBLIC_KEY"),
    # url_endpoint=os.environ.get("IMAGEKIT_URL"),
)


def get_image_caption(imgUrl: str):
    invoke_url = "https://integrate.api.nvidia.com/v1/chat/completions"
    stream = False
    image_bytes = requests.get(imgUrl).content
    imageBase64 = base64.b64encode(image_bytes).decode()
    headers = {
        "Authorization": f"Bearer {os.environ.get("NVIDIA_API_KEY")}",
        "Accept": "text/event-stream" if stream else "application/json",
    }

    payload = {
        "model": "mistralai/mistral-medium-3-instruct",
        "messages": [
            {
                "role": "system",
                "content": "You are an professional image analizer and caption generator, Your only task is to generate a proper meaningfull caption for the givne image maximum 4 to 6 words. First take a good detailing look then just generate caption",
            },
            {
                "role": "user",
                "content": f'Do for this image <img src="data:image/jpeg;base64,{imageBase64}" />',
            },
        ],
        "max_tokens": 512,
        "temperature": 1.00,
        "top_p": 1.00,
        "frequency_penalty": 0.00,
        "presence_penalty": 0.00,
        "stream": stream,
    }

    response = requests.post(invoke_url, headers=headers, json=payload)

    if stream:
        for line in response.iter_lines():
            if line:
                print(line.decode("utf-8"))
    else:
        final_result = response.json()['choices']
        return final_result[0]['message']['content']


get_image_caption(
    "https://ik.imagekit.io/taqui/python/3biy1ann6z4g1_kM_cAqdLk.jpeg?updatedAt=1776695712529"
)

