from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from fastapi.openapi.docs import get_redoc_html, get_swagger_ui_html
from fastapi.openapi.utils import get_openapi
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from sqlmodel import SQLModel

from config import engine
from core.models.user import User
from routers import bins, search, views, waste_materials
from routers.auth import get_current_user
from routers.limiter import limiter


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    SQLModel.metadata.create_all(engine)
    yield
    # shutdown logic


app = FastAPI(
    title="BinBuddyKorea API",
    lifespan=lifespan,
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
)

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

app.add_middleware(GZipMiddleware)

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


@app.get("/docs", include_in_schema=False)
def get_swagger_ui_documentation(
    user: User = Depends(get_current_user),
) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


@app.get("/redoc", include_in_schema=False)
def get_redoc_documentation(user: User = Depends(get_current_user)) -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="docs")


@app.get("/openapi.json", include_in_schema=False)
def openapi(user: User = Depends(get_current_user)):
    return get_openapi(title="FastAPI", version="0.1.0", routes=app.routes)
