import requests
from dotenv import load_dotenv
import os
from langchain_nvidia_ai_endpoints import ChatNVIDIA

load_dotenv()

api_key = os.getenv("NVIDIA_API_KEY")


def get_weather_data(longitude: int, latitude: int):

    url = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m"
    res = requests.get(url)
    data = res.json()
    return data


# client = ChatNVIDIA(
#     model="stepfun-ai/step-3.5-flash",
#     api_key=api_key,
#     temperature=1,
#     top_p=0.9,
#     max_completion_tokens=16384,
# )

# def basic_chat(userMsg: str):
#     client = ChatNVIDIA(
#         model="minimaxai/minimax-m2.7",
#         api_key=api_key,
#         temperature=1,
#         top_p=0.9,
#         max_completion_tokens=16384,
#     )

#     for chunk in client.generate([{"role": "user", "content": userMsg}]):
#         print(chunk.content, end="")


# basic_chat("what's your name")
# result = client.invoke("What is your name?")
# print(result.content)