from datetime import datetime

from sqlmodel import SQLModel

from core.schemas.waste_material import WasteMaterialOutput


class BinInput(SQLModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"


class BinOutput(BinInput):
    id: int
    created_at: datetime
    updated_at: datetime
    waste_materials: list[WasteMaterialOutput] = []
