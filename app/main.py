from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from app.api import router

app = FastAPI(title="Recipe API")

# Mount the static folder
app.mount("/static", StaticFiles(directory="app/static"), name="static")

app.include_router(router)

@app.get("/")
def home():
    # Return the UI instead of JSON
    return FileResponse("app/static/index.html")
