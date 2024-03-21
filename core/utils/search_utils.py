from sqlmodel import Session, col, func, or_, select

from core.models.waste_material import WasteMaterial
from core.schemas.waste_material import WasteMaterialSearchResult


class SearchUtils:
    @staticmethod
    def find_waste_materials_by_name_and_description(
        q: str, limit: int, session: Session
    ) -> list[WasteMaterialSearchResult]:
        """Find waste materials by name and description in database"""

        statement = (
            select(WasteMaterial)
            .where(
                or_(
                    func.lower(col(WasteMaterial.name_en)).contains(q.lower()),
                    (col(WasteMaterial.name_kr).contains(q)),
                    func.lower(col(WasteMaterial.description)).contains(q.lower()),
                )
            )
            .limit(limit)
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
