from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from schemas import (
    WasteMaterial,
    WasteMaterialInput,
    WasteMaterialOutput,
    load_db,
    save_db,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    SQLModel.metadata.create_all(engine)
    yield
    # shutdown logic


app = FastAPI(title="BinBuddyKorea API", lifespan=lifespan)

db = load_db()

engine = create_engine(
    "sqlite:///binbuddykorea.db",
    connect_args={"check_same_thread": False},  # Needed for SQLite
    echo=True,  # Log generated SQL (to remove)
)


def get_session():
    with Session(engine) as session:
        yield session


@app.get("/api/waste-materials")
def get_waste_materials(
    recyclable: bool | None = None, session: Session = Depends(get_session)
) -> list:
    query = select(WasteMaterial)

    if isinstance(recyclable, bool):
        query = query.where(WasteMaterial.recyclable == recyclable)

    return list(session.exec(query).all())


@app.get("/api/waste-materials/{id}")
def get_waste_material_by_id(id: int) -> dict:
    for waste_material in db:
        if waste_material.id == id:
            return waste_material.dict()
    raise HTTPException(status_code=404, detail=f"No waste material found with id={id}")


@app.post("/api/waste-materials", response_model=WasteMaterial)
def add_waste_material(
    waste_material_input: WasteMaterialInput, session: Session = Depends(get_session)
) -> WasteMaterial:
    with Session(engine) as session:
    new_waste_material = WasteMaterial.model_validate(waste_material_input)
    session.add(new_waste_material)
    session.commit()
    session.refresh(new_waste_material)
    return new_waste_material


@app.delete("/api/waste-materials/{id}", status_code=204)
def delete_waste_material(id: int) -> None:
    for waste_material in db:
        if waste_material.id == id:
            db.remove(waste_material)
            save_db(db)
            return
    raise HTTPException(status_code=404, detail=f"No waste material with id={id}")


@app.put("/api/waste-materials/{id}", response_model=WasteMaterialOutput)
def change_waste_material(id: int, new_data: WasteMaterialInput) -> WasteMaterialOutput:
    for waste_material in db:
        if waste_material.id == id:
            waste_material.name_en = new_data.name_en
            waste_material.name_kr = new_data.name_kr
            waste_material.description = new_data.description
            waste_material.recyclable = new_data.recyclable
            save_db(db)
            return waste_material
    raise HTTPException(status_code=404, detail=f"No waste material with id={id}")
