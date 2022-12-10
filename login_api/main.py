from fastapi import FastAPI
from login_api.views import routes


app = FastAPI()
app.include_router(routes)

