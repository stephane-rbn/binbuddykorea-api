from sqlmodel import SQLModel

from core.schemas.waste_material import WasteMaterialOutput


class BinInput(SQLModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"


class BinOutput(BinInput):
    id: int
    waste_materials: list[WasteMaterialOutput] = []
