from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import engine, Base
from .routers import post_router, comment_router
from .seed import seed_initial_data

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Community API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post_router)
app.include_router(comment_router)


@app.on_event("startup")
def on_startup():
    seed_initial_data()
