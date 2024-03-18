import uuid


class CustomUtils:
    @staticmethod
    def generate_uuid(prefix: str) -> str:
        return prefix + str(uuid.uuid4())
