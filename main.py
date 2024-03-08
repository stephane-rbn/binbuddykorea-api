from fastapi import FastAPI, HTTPException

from schemas import load_db

app = FastAPI()

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
