import os
import random

from faker import Faker
from sqlmodel import Session

from config import get_session
from core.models.bin import Bin
from core.models.waste_material import WasteMaterial
from core.schemas.waste_material import WasteMaterialInput
from core.utils.slug_utils import SlugUtils

BIN_NAMES_DICT = {
    "General Waste": "일반쓰레기",
    "PET bottles": "PET병",
    "Clear plastic bottle": "투명 페트병",
    "Color plastic bottle": "유색 페트병",
    "Plastic": "플라스틱류",
    "Vinyl": "비닐류",
    "Can": "캔류",
    "Paper": "종이류",
    "Glass bottle": "유리병",
    "Food waste": "음식물 쓰레기",
    "Waste battery collection box": "전지류 (폐건전지 수거함)",
    "Recyclable waste": "재활용 쓰레기",
    "Place directly on the ground next to the recycling bins (no plastic bag)": "재활용통 옆에 플라스틱 봉투 안이 아니라 바닥에 직접 둠",
    "Report to the local district office": "구청에 신고함",
    "Report to the local community center": "주민센터에 신고함",
}

fake = Faker()
fake_ko = Faker("ko_KR")


class Seeds:
    @staticmethod
    def load_fake_data() -> None:
        session: Session = next(get_session())

        for name_en, name_kr in BIN_NAMES_DICT.items():
            bin_name_en = name_en
            bin_name_kr = name_kr
            bin_slug = SlugUtils.generate_slug(name_en)
            bin_description = fake.text()

            bin_instance = Bin(
                name_en=bin_name_en,
                name_kr=bin_name_kr,
                description=bin_description,
                slug=bin_slug,
            )

            new_bin = Bin.model_validate(bin_instance)

            session.add(new_bin)
            session.commit()
            session.refresh(new_bin)

            waste_materials_count = 20

            for _ in range(waste_materials_count):
                random_name_en = " ".join(fake.words(3)).capitalize()

                waste_material_name_en = random_name_en
                waste_material_name_kr = fake_ko.catch_phrase()
                waste_material_slug = SlugUtils.generate_slug(random_name_en)
                waste_material_description = fake.text()
                waste_material_recycle = bool(random.getrandbits(1))

                waste_material_instance = WasteMaterialInput(
                    name_en=waste_material_name_en,
                    name_kr=waste_material_name_kr,
                    description=waste_material_description,
                    recyclable=waste_material_recycle,
                )

                new_waste_material = WasteMaterial.model_validate(
                    waste_material_instance, update={"slug": waste_material_slug}
                )

                # Purposely not assigning last waste material to any bin
                if _ < (waste_materials_count - 1):
                    new_bin.waste_materials.append(new_waste_material)

                session.add(new_waste_material)
                session.commit()


if __name__ == "__main__":
    if eval(os.getenv("ENV_TEST").lower().capitalize()):  # type: ignore  # noqa: S307
        Seeds.load_fake_data()
