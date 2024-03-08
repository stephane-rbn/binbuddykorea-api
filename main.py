from fastapi import FastAPI, HTTPException

from schemas import WasteMaterialInput, WasteMaterialOutput, load_db, save_db

app = FastAPI(title="BinBuddyKorea API")

db = load_db()


@app.get("/api/waste-materials")
def get_waste_materials(recyclable: bool | None = None) -> list:
    if isinstance(recyclable, bool):
        matching_records = []
        for waste_material in db:
            if waste_material.recyclable == recyclable:
                matching_records.append(waste_material)
        return matching_records
    else:
        return db


@app.get("/api/waste-materials/{id}")
def get_waste_material_by_id(id: int) -> dict:
    for waste_material in db:
        if waste_material.id == id:
            return waste_material.dict()
    raise HTTPException(status_code=404, detail=f"No waste material found with id={id}")


@app.post("/api/waste-materials", response_model=WasteMaterialOutput)
def add_waste_material(waste_material: WasteMaterialInput) -> WasteMaterialOutput:
    new_waste_material = WasteMaterialOutput(
        id=len(db) + 1,
        name_en=waste_material.name_en,
        name_kr=waste_material.name_kr,
        description=waste_material.description,
        recyclable=waste_material.recyclable,
    )
    db.append(new_waste_material)
    save_db(db)
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
