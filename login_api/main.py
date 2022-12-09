from fastapi import FastAPI
from views import routes


app = FastAPI()
app.include_router(routes)
