# coding=utf-8


#-------------------------------------------------------------------------------------------------#


from sqlmodel import Session, SQLModel, create_engine
from dotenv import load_dotenv
from os import getenv


#-------------------------------------------------------------------------------------------------#


load_dotenv()


DATABASE_TYPE = getenv("DATABASE_TYPE")

if DATABASE_TYPE == "sqlite":
    SQLITE_DATABASE_NAME = getenv("SQLITE_DATABASE_NAME")
    sqlite_url = f"sqlite:///{SQLITE_DATABASE_NAME}"

    connect_args = {"check_same_thread": False}
    engine = create_engine(sqlite_url, echo=True, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_session():
    with Session(engine) as session:
        yield session


def get_session_2():
    with Session(engine) as session:
        return session


#-------------------------------------------------------------------------------------------------#

