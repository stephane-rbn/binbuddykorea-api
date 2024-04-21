"""
create_user.py
-------------
A convenience script to create a user.
"""

import os
from getpass import getpass

from dotenv import load_dotenv
from sqlmodel import Session, SQLModel, create_engine

from core.models.user import User

load_dotenv()

DATABASE_URL = f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOSTNAME')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

engine = create_engine(
    DATABASE_URL,
    echo=eval(os.getenv("DISPLAY_SQL_LOGS").lower().capitalize()),  # type: ignore  # noqa: S307
)

if __name__ == "__main__":
    print("Creating tables (if necessary)")
    SQLModel.metadata.create_all(engine)

    print("--------")

    print("This script will create a user and save it in the database.")

    username = input("Please enter username\n")
    pwd = getpass("Please enter password\n")

    with Session(engine) as session:
        user = User(username=username)
        user.set_password(pwd)
        session.add(user)
        session.commit()
