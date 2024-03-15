from contextlib import asynccontextmanager

from fastapi import FastAPI
from sqlmodel import SQLModel

from config import engine
from routers import bins, waste_materials


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    SQLModel.metadata.create_all(engine)
    yield
    # shutdown logic


app = FastAPI(title="BinBuddyKorea API", lifespan=lifespan)
app.include_router(bins.router, tags=["Bins"])
app.include_router(waste_materials.router, tags=["Waste Materials"])
