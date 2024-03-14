from sqlmodel import Field, Relationship, SQLModel


class WasteMaterialInput(SQLModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"
    recyclable: bool | None = True


class WasteMaterialOutput(WasteMaterialInput):
    id: int


class WasteMaterial(WasteMaterialInput, table=True):
    __tablename__: str = "waste_materials"
    id: int | None = Field(default=None, primary_key=True)
    bin_id: int | None = Field(default=None, foreign_key="bins.id")
    bin: "Bin" = Relationship(back_populates="waste_materials")


class BinInput(SQLModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"


class BinOutput(BinInput):
    id: int
    waste_materials: list[WasteMaterialOutput] = []


class Bin(BinInput, table=True):
    __tablename__: str = "bins"
    id: int | None = Field(default=None, primary_key=True)
    waste_materials: list[WasteMaterial] = Relationship(back_populates="bin")
