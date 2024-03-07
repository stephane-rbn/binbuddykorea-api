from fastapi import FastAPI, HTTPException

app = FastAPI()

db = [
    {
        "id": 1,
        "name_en": "Plastic",
        "name_kr": "플라스틱",
        "description": "Plastic waste includes bottles, bags, containers, and packaging materials.",
        "recyclable": True,
    },
    {
        "id": 2,
        "name_en": "Paper",
        "name_kr": "종이",
        "description": "Paper waste consists of newspapers, magazines, cardboard, and office paper.",
        "recyclable": True,
    },
    {
        "id": 3,
        "name_en": "Glass",
        "name_kr": "유리",
        "description": "Glass waste includes bottles, jars, and broken glass objects.",
        "recyclable": True,
    },
    {
        "id": 4,
        "name_en": "Metal",
        "name_kr": "금속",
        "description": "Metal waste consists of aluminum cans, steel, iron, and other metallic items.",
        "recyclable": True,
    },
    {
        "id": 5,
        "name_en": "Organic",
        "name_kr": "유기물",
        "description": "Organic waste includes food scraps, yard waste, and other biodegradable materials.",
        "recyclable": True,
    },
    {
        "id": 6,
        "name_en": "Electronic",
        "name_kr": "전자제품",
        "description": "Electronic waste (e-waste) includes old computers, phones, TVs, and other electronic devices.",
        "recyclable": False,
    },
    {
        "id": 7,
        "name_en": "Textile",
        "name_kr": "섬유",
        "description": "Textile waste comprises clothing, fabrics, and other textiles that are no longer usable.",
        "recyclable": True,
    },
    {
        "id": 8,
        "name_en": "Hazardous",
        "name_kr": "유해물질",
        "description": "Hazardous waste includes chemicals, batteries, and other materials that pose a risk to health or the environment.",
        "recyclable": False,
    },
    {
        "id": 9,
        "name_en": "Medical",
        "name_kr": "의료폐기물",
        "description": "Medical waste consists of used needles, syringes, bandages, and other biomedical materials.",
        "recyclable": False,
    },
]


@app.get("/api/waste-materials")
def get_waste_materials(recyclable: bool | None = None) -> list:
    if isinstance(recyclable, bool):
        matching_records = []
        for waste_material in db:
            if waste_material["recyclable"] == recyclable:
                matching_records.append(waste_material)
        return matching_records
    else:
        return db


@app.get("/api/waste-materials/{id}")
def get_waste_material_by_id(id: int) -> dict:
    for waste_material in db:
        if waste_material["id"] == id:
            return waste_material

    raise HTTPException(status_code=404, detail=f"No waste material found with id={id}")
