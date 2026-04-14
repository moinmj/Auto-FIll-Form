from fastapi import FastAPI
from app.routes import form_routes

app = FastAPI()

app.include_router(form_routes.router)

@app.get("/")
def home():
    return {"message": "Smart Form AI is running"}