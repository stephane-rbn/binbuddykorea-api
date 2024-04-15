from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlmodel import SQLModel

from config import engine
from routers import bins, search, views, waste_materials
from routers.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    SQLModel.metadata.create_all(engine)
    yield
    # shutdown logic


app = FastAPI(title="BinBuddyKorea API", lifespan=lifespan)

app.state.limiter = limiter

app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)  # type: ignore

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(bins.router, tags=["Bins"])
app.include_router(waste_materials.router, tags=["Waste Materials"])
app.include_router(search.router, tags=["Search"])
app.include_router(views.router, tags=["Templates"])


@app.middleware("http")
async def add_bins_cookie(request: Request, call_next):
    response = await call_next(request)
    response.set_cookie(key="bins_cookie", value="you_visited_binbuddykorea_app")
    return response
