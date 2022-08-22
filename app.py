
from fastapi import FastAPI
from dotenv import load_dotenv
from routes.manage import manage
from prometheus_fastapi_instrumentator import Instrumentator

load_dotenv()
app = FastAPI()
app.include_router(manage, prefix="/manage")
Instrumentator().instrument(app).expose(app)
