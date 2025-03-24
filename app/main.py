from fastapi import FastAPI

from . import models, database, endpoints

models.Base.metadata.create_all(bind=database.engine)

app = FastAPI()

app.include_router(endpoints.router)
