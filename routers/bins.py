from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from config import get_session
from core.models.bin import Bin
from core.schemas.bin import BinInput, BinOutput

router = APIRouter(prefix="/api/v1/bins")


@router.get("/")
def get_bins(session: Session = Depends(get_session)) -> list:
    query = select(Bin)
    return list(session.exec(query).all())


@router.get("/{id}", response_model=BinOutput)
def get_bin_by_id(id: int, session: Session = Depends(get_session)) -> Bin:
    bin = session.get(Bin, id)

    if bin:
        return bin

    raise HTTPException(status_code=404, detail=f"No bin found with id={id}")


@router.post("/", response_model=Bin)
def add_bin(bin_input: BinInput, session: Session = Depends(get_session)) -> Bin:
    new_bin = Bin.model_validate(bin_input)
    session.add(new_bin)
    session.commit()
    session.refresh(new_bin)
    return new_bin


@router.delete("/{id}", status_code=204)
def delete_bin_by_id(id: int, session: Session = Depends(get_session)) -> None:
    bin = session.get(Bin, id)

    if bin:
        session.delete(bin)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No bin with id={id}")


@router.put("/{id}", response_model=Bin)
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
