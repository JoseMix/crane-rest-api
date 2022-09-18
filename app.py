
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.manage import manage

load_dotenv()
app = FastAPI()
app.include_router(manage, prefix="/manage")
