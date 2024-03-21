from slugify import slugify


class SlugUtils:
    @staticmethod
    def generate_slug(text: str) -> str:
        return slugify(text, max_length=80, word_boundary=True)
