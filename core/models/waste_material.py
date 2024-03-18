from datetime import datetime

import sqlalchemy as sa
from sqlmodel import Field, Relationship

from core.schemas.waste_material import WasteMaterialInput
from core.utils.custom_utils import CustomUtils


class WasteMaterial(WasteMaterialInput, table=True):
    __tablename__: str = "waste_materials"
    id: int | None = Field(default=None, primary_key=True)
    uuid: str = Field(
        default=CustomUtils.generate_uuid("wm_"),
        nullable=False,
        unique=True,
    )
    slug: str = Field(nullable=False, unique=True)
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
    bin: "Bin" = Relationship(back_populates="waste_materials")  # type: ignore # noqa: F821
