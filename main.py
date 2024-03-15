import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv
from fastapi import Depends, FastAPI, HTTPException
from sqlmodel import Session, SQLModel, create_engine, select

from schemas import Bin, BinInput, BinOutput, WasteMaterial, WasteMaterialInput

load_dotenv()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # startup logic
    SQLModel.metadata.create_all(engine)
    yield
    # shutdown logic


app = FastAPI(title="BinBuddyKorea API", lifespan=lifespan)

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOSTNAME')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(DATABASE_URL, echo=True)


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


@app.get("/api/waste-materials/{id}", response_model=WasteMaterial)
def get_waste_material_by_id(
    id: int, session: Session = Depends(get_session)
) -> WasteMaterial:
    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        return waste_material

    raise HTTPException(status_code=404, detail=f"No waste material found with id={id}")


@app.delete("/api/waste-materials/{id}", status_code=204)
def delete_waste_material(id: int, session: Session = Depends(get_session)) -> None:
    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        session.delete(waste_material)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No waste material with id={id}")


@app.put("/api/waste-materials/{id}", response_model=WasteMaterial)
def change_waste_material(
    id: int, new_data: WasteMaterialInput, session: Session = Depends(get_session)
) -> WasteMaterial:
    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        waste_material.name_en = new_data.name_en
        waste_material.name_kr = new_data.name_kr
        waste_material.description = new_data.description
        waste_material.recyclable = new_data.recyclable
        session.commit()
        return waste_material

    raise HTTPException(status_code=404, detail=f"No waste material with id={id}")


@app.get("/api/bins")
def get_bins(session: Session = Depends(get_session)) -> list:
    query = select(Bin)
    return list(session.exec(query).all())


@app.get("/api/bins/{id}", response_model=BinOutput)
def get_bin_by_id(id: int, session: Session = Depends(get_session)) -> Bin:
    bin = session.get(Bin, id)

    if bin:
        return bin

    raise HTTPException(status_code=404, detail=f"No bin found with id={id}")


@app.delete("/api/bins/{id}", status_code=204)
def delete_bin_by_id(id: int, session: Session = Depends(get_session)) -> None:
    bin = session.get(Bin, id)

    if bin:
        session.delete(bin)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No bin with id={id}")


@app.put("/api/bins/{id}", response_model=Bin)
def change_bin(
    id: int, new_data: BinInput, session: Session = Depends(get_session)
) -> Bin:
    bin = session.get(Bin, id)

    if bin:
        bin.name_en = new_data.name_en
        bin.name_kr = new_data.name_kr
        bin.description = new_data.description
        session.commit()
        return bin

    raise HTTPException(status_code=404, detail=f"No bin with id={id}")


@app.post("/api/bins", response_model=Bin)
def add_bin(bin_input: BinInput, session: Session = Depends(get_session)) -> Bin:
    new_bin = Bin.model_validate(bin_input)
    session.add(new_bin)
    session.commit()
    session.refresh(new_bin)
    return new_bin


@app.post("/api/bins/{bin_id}/waste-materials", response_model=Bin)
def add_waste_material_to_bin(
    bin_id: int,
    waste_material_input: WasteMaterialInput,
    session: Session = Depends(get_session),
) -> WasteMaterial:
    bin = session.get(Bin, bin_id)

    if bin:
        new_waste_material = WasteMaterial.model_validate(
            waste_material_input, update={"bin_id": bin_id}
        )
        bin.waste_materials.append(new_waste_material)
        session.commit()
        session.refresh(new_waste_material)
        return new_waste_material

    raise HTTPException(status_code=404, detail=f"No bin with id={bin_id}")
