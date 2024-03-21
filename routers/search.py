from fastapi import APIRouter, Depends, Query
from sqlmodel import Session

from config import get_session
from core.schemas.waste_material import WasteMaterialSearchResult
from core.utils.search_utils import SearchUtils

router = APIRouter(prefix="/api/v1/search")


@router.get("/", response_model=list[WasteMaterialSearchResult])
def search_waste_materials(
    q: str | None = Query(..., min_length=1, description="Search waste material"),
    session: Session = Depends(get_session),
) -> list[WasteMaterialSearchResult]:
    """Search waste materials"""

    if q is None:
        return []

    return SearchUtils.find_waste_materials_by_name_and_description(q, 5, session)
