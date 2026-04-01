from fastapi import FastAPI
from api.routes import router

app = FastAPI(title="ScoreMe Decision System")

app.include_router(router)

@app.get("/")
def home():
    return {"message": "Decision System Running 🚀"}