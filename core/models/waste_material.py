from datetime import datetime

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from core.schemas.waste_material import WasteMaterialInput


class WasteMaterial(WasteMaterialInput, table=True):
    __tablename__: str = "waste_materials"
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
    bin_id: int | None = Field(default=None, foreign_key="bins.id")
    bin: "Bin" = Relationship(back_populates="waste_materials")
