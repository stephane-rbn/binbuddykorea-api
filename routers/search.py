from fastapi import APIRouter, Cookie, Depends, Query, Request
from sqlmodel import Session

from config import get_session
from core.schemas.waste_material import WasteMaterialSearchResult
from core.utils.search_utils import SearchUtils

from .limiter import limiter

router = APIRouter(prefix="/api/v1/search")


@router.get("/", response_model=list[WasteMaterialSearchResult])
@limiter.limit("20/second")
def search_waste_materials(
    request: Request,
    q: str = Query(None, description="Search waste material"),
    session: Session = Depends(get_session),
    bins_cookie: str | None = Cookie(None),
) -> list[WasteMaterialSearchResult]:
    """Search waste materials"""

    print(bins_cookie)

    if q is None or q == "":
        return []

    return SearchUtils.find_waste_materials_by_name_and_description(q, 5, session)
