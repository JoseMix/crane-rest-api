
from fastapi import FastAPI
from dotenv import load_dotenv
#from clients import DockerClient

from routes.manage import manage

load_dotenv()  # take environment variables from .env.

app = FastAPI()

app.include_router(manage, prefix="/manage")