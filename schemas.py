import json

from pydantic import BaseModel


class WasteMaterialInput(BaseModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"
    recyclable: bool | None = True


class WasteMaterialOutput(WasteMaterialInput):
    id: int


class BinInput(BaseModel):
    name_en: str
    name_kr: str
    description: str | None = "Todo"


class BinOutput(BinInput):
    id: int
    waste_materials: list[WasteMaterialOutput] = []


def load_db() -> list[WasteMaterialOutput]:
    """Load a list of WasteMaterial objects from a JSON file"""
    with open("waste-materials.json") as f:
        json_data = json.load(f)

        waste_materials = []

        for obj in json_data:
            waste_material = WasteMaterialOutput.model_validate(obj)
            waste_materials.append(waste_material)

        return waste_materials


def save_db(waste_materials: list[WasteMaterialInput]) -> None:
    """Save a list of new WasteMaterial objects in JSON file"""
    with open("waste-materials.json", "w") as f:
        converted_dictionaries = []

        for waste_material in waste_materials:
            converted_dictionaries.append(waste_material.dict())

        json.dump(converted_dictionaries, f, indent=4)
