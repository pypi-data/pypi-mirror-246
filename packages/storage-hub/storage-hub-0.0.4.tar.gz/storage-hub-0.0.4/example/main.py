from fastapi import FastAPI
from fastapi_storage.settings import settings


def get_application():
    settings.init()
    application = FastAPI()
    return application


app = get_application()


@app.get("/")
def read_root():
    return {"Hello": "World"}
