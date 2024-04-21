from fastapi import APIRouter, Depends, HTTPException, Request
from slugify import slugify
from sqlmodel import Session, select

from config import get_session
from core.models.bin import Bin
from core.models.user import User
from core.schemas.bin import BinInput, BinOutput
from routers.auth import get_current_user

from .limiter import limiter

router = APIRouter(prefix="/api/v1/bins")


@router.get("/")
@limiter.limit("1/second")
def get_bins(
    request: Request,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> list:
    """Get all bins from the database."""

    query = select(Bin)
    return list(session.exec(query).all())


@router.get("/{id}", response_model=BinOutput)
@limiter.limit("10/second")
def get_bin_by_id(
    request: Request,
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Bin:
    """Get a bin by its id."""

    bin = session.get(Bin, id)

    if bin:
        return bin

    raise HTTPException(status_code=404, detail=f"No bin found with id={id}")


@router.post("/", response_model=Bin)
@limiter.limit("1/second")
def add_bin(
    request: Request,
    bin_input: BinInput,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Bin:
    """Add a new bin to the database."""

    slug = slugify(bin_input.name_en, max_length=80, word_boundary=True)

    new_bin = Bin.model_validate(bin_input, update={"slug": slug})

    session.add(new_bin)
    session.commit()
    session.refresh(new_bin)
    return new_bin


@router.delete("/{id}", status_code=204)
@limiter.limit("1/second")
def delete_bin_by_id(
    request: Request,
    id: int,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> None:
    """Delete a bin by its id."""

    bin = session.get(Bin, id)

    if bin:
        session.delete(bin)
        session.commit()
    else:
        raise HTTPException(status_code=404, detail=f"No bin with id={id}")


@router.put("/{id}", response_model=Bin)
@limiter.limit("1/second")
def change_bin(
    request: Request,
    id: int,
    new_data: BinInput,
    session: Session = Depends(get_session),
    user: User = Depends(get_current_user),
) -> Bin:
    """Update a bin by its id."""

    bin = session.get(Bin, id)

    if bin:
        bin.name_en = new_data.name_en
        bin.name_kr = new_data.name_kr
        bin.description = new_data.description
        session.commit()
        session.refresh(bin)
        return bin

    raise HTTPException(status_code=404, detail=f"No bin with id={id}")
