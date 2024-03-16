from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from config import get_session
from core.models.bin import Bin
from core.models.waste_material import WasteMaterial
from core.schemas.waste_material import WasteMaterialInput

router = APIRouter(prefix="/api/v1/waste-materials")


@router.get("/")
def get_waste_materials(
    recyclable: bool | None = None, session: Session = Depends(get_session)
) -> list:
    query = select(WasteMaterial)

    if isinstance(recyclable, bool):
        query = query.where(WasteMaterial.recyclable == recyclable)

    return list(session.exec(query).all())


@router.get("/{id}", response_model=WasteMaterial)
def get_waste_material_by_id(
    id: int, session: Session = Depends(get_session)
) -> WasteMaterial:
    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        return waste_material

    raise HTTPException(status_code=404, detail=f"No waste material found with id={id}")


@router.post("/", response_model=WasteMaterial)
def add_waste_material(
    waste_material_input: WasteMaterialInput,
    session: Session = Depends(get_session),
) -> WasteMaterial:
    bin_id = waste_material_input.bin_id

    if bin_id is not None:
        bin = session.get(Bin, bin_id)
        if not bin:
            raise HTTPException(status_code=404, detail=f"No bin with id={bin_id}")

    new_waste_material = WasteMaterial.model_validate(waste_material_input)

    if bin_id is not None:
        bin.waste_materials.append(new_waste_material)

    session.add(new_waste_material)
    session.commit()
    session.refresh(new_waste_material)
    return new_waste_material


@router.delete("/{id}", status_code=204)
def delete_waste_material(id: int, session: Session = Depends(get_session)) -> None:
    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        session.delete(waste_material)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No waste material with id={id}")


@router.put("/{id}", response_model=WasteMaterial)
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
