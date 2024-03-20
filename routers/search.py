from fastapi import APIRouter, Depends, Query
from sqlmodel import Session, col, func, or_, select

from config import get_session
from core.models.waste_material import WasteMaterial
from core.schemas.waste_material import WasteMaterialSearchResult

router = APIRouter(prefix="/api/v1/search")


@router.get("/", response_model=list[WasteMaterialSearchResult])
def search_waste_materials_by_name_and_description(
    q: str = Query(..., min_length=1, description="Search term"),
    session: Session = Depends(get_session),
) -> list[WasteMaterialSearchResult]:
    """Search waste materials by name and description."""

    statement = (
        select(WasteMaterial)
        .where(
            or_(
                func.lower(col(WasteMaterial.name_en)).contains(q.lower()),
                (col(WasteMaterial.name_kr).contains(q)),
                func.lower(col(WasteMaterial.description)).contains(q.lower()),
            )
        )
        .limit(5)
    )

    results = session.exec(statement).all()
    suggestions: list[WasteMaterialSearchResult] = []

    for result in results:
        suggestions.append(
            WasteMaterialSearchResult(
                name_en=result.name_en,
                name_kr=result.name_kr,
                description=result.description,
            )
        )

    return suggestions
