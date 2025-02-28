from fastapi import FastAPI
from app.routes import restaurant, consumer, estimation
from app.database import Base, engine

app = FastAPI()
Base.metadata.create_all(bind=engine)

app.include_router(restaurant.router)
app.include_router(consumer.router)
app.include_router(estimation.router)


@app.get("/")
def read_root():
    return {"message": "FastAPI is running"}
