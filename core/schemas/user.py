from sqlmodel import SQLModel


class UserOutput(SQLModel):
    id: int
    username: str
