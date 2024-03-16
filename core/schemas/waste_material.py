from datetime import datetime

from sqlmodel import SQLModel


class WasteMaterialInput(SQLModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"
    recyclable: bool | None = True
    bin_id: int | None = None


class WasteMaterialOutput(WasteMaterialInput):
    id: int
    created_at: datetime
    updated_at: datetime
