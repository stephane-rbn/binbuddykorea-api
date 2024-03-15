from datetime import datetime

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from core.models.waste_material import WasteMaterial
from core.schemas.bin import BinInput


class Bin(BinInput, table=True):
    __tablename__: str = "bins"
    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"server_default": sa.func.now()},
        nullable=False,
    )
    updated_at: datetime | None = Field(
        default=None,
        sa_type=sa.DateTime(timezone=True),
        sa_column_kwargs={"onupdate": sa.func.now(), "server_default": sa.func.now()},
    )
    waste_materials: list[WasteMaterial] = Relationship(back_populates="bin")
