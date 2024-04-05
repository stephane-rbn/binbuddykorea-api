from fastapi import APIRouter, Depends, HTTPException, Request
from slugify import slugify
from sqlmodel import Session, select

from config import get_session
from core.models.bin import Bin
from core.models.waste_material import WasteMaterial
from core.schemas.waste_material import WasteMaterialInput, WasteMaterialOutput

from .limiter import limiter

router = APIRouter(prefix="/api/v1/waste-materials")


@router.get("/")
@limiter.limit("1/second")
def get_waste_materials(
    request: Request,
    recyclable: bool | None = None,
    session: Session = Depends(get_session),
) -> list:
    """Get all waste materials from the database with limit of 25. Optionally filter by recyclable."""

    limit = 25

    query = select(WasteMaterial).limit(limit)

    if isinstance(recyclable, bool):
        query = query.where(WasteMaterial.recyclable == recyclable).limit(limit)

    return list(session.exec(query).all())


@router.get("/{id}", response_model=WasteMaterialOutput)
@limiter.limit("1/second")
def get_waste_material_by_id(
    request: Request, id: int, session: Session = Depends(get_session)
) -> WasteMaterial:
    """Get a waste material by its id."""

    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        return waste_material

    raise HTTPException(status_code=404, detail=f"No waste material found with id={id}")


@router.post("/", response_model=WasteMaterial)
@limiter.limit("1/second")
def add_waste_material(
    request: Request,
    waste_material_input: WasteMaterialInput,
    session: Session = Depends(get_session),
) -> WasteMaterial:
    """Add a new waste material to the database. Optionally assign it to a bin."""

    bin_id = waste_material_input.bin_id

    if bin_id is not None:
        bin = session.get(Bin, bin_id)
        if not bin:
            raise HTTPException(status_code=404, detail=f"No bin with id={bin_id}")

    slug = slugify(waste_material_input.name_en, max_length=80, word_boundary=True)

    new_waste_material = WasteMaterial.model_validate(
        waste_material_input, update={"slug": slug}
    )

    if bin_id is not None:
        bin.waste_materials.append(new_waste_material)

    session.add(new_waste_material)
    session.commit()
    session.refresh(new_waste_material)
    return new_waste_material


@router.delete("/{id}", status_code=204)
@limiter.limit("1/second")
def delete_waste_material(
    request: Request, id: int, session: Session = Depends(get_session)
) -> None:
    """Delete a waste material by its id."""

    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        session.delete(waste_material)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No waste material with id={id}")


@router.put("/{id}", response_model=WasteMaterial)
@limiter.limit("1/second")
def change_waste_material(
    request: Request,
    id: int,
    new_data: WasteMaterialInput,
    session: Session = Depends(get_session),
) -> WasteMaterial:
    """Update a waste material by its id."""

    waste_material = session.get(WasteMaterial, id)

    if waste_material:
        waste_material.name_en = new_data.name_en
        waste_material.name_kr = new_data.name_kr
        waste_material.description = new_data.description
        waste_material.recyclable = new_data.recyclable
        waste_material.slug = slugify(
            new_data.name_en, max_length=80, word_boundary=True
        )
        session.commit()
        session.refresh(waste_material)
        return waste_material

    raise HTTPException(status_code=404, detail=f"No waste material with id={id}")
