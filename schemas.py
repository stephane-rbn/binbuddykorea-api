import json

from pydantic import BaseModel


class WasteMaterial(BaseModel):
    id: int
    name_en: str
    name_kr: str
    description: str | None = "Todo"
    recyclable: bool | None = True


def load_db() -> list[WasteMaterial]:
    """Load a list of WasteMaterial objects from a JSON file"""
    with open("waste-materials.json") as f:
        json_data = json.load(f)

        waste_materials = []

        for obj in json_data:
            waste_material = WasteMaterial.model_validate(obj)
            waste_materials.append(waste_material)

        return waste_materials
