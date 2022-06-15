
from fastapi import FastAPI
from dotenv import load_dotenv
from clients import DockerClient

load_dotenv()  # take environment variables from .env.

app = FastAPI()

@app.get('/')
def read_root():
    return {"Hellooo": "World"}
