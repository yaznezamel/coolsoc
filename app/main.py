from fastapi import FastAPI
from app import __version__
import app.db.models.post as post_models
import app.db.models.user as user_models
from app.db.database import engine
from app.router import api_router

post_models.Base.metadata.create_all(bind=engine)
user_models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="coolsoc", version=__version__)

app.include_router(api_router)

@app.get("/")
def root(): 
    return {"message": "Welcome to cool social application"}