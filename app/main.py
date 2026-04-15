from fastapi import FastAPI
from app.database import Base, engine
from app.routers import user_router
from app.routers import auth_router  # 🔹 yeni

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RESTful API", version="1.0.0")

app.include_router(user_router.router)
app.include_router(auth_router.router)  # 🔹 yeni

@app.get("/")
def root():
    return {"message": "FastAPI çalışıyor", "status": "ok"}
