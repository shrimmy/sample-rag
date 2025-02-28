from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import uvicorn

app = FastAPI()

app.mount("/", StaticFiles(directory="src/static", html=True), name="static")
