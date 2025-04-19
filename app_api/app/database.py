from typing import Annotated
from fastapi import Depends
from sqlmodel import SQLModel, Session, create_engine

engine = create_engine("postgresql+psycopg2://app:password@db/app")

#                                           driver://user:password@host/db
def init_database():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDeps = Annotated[Session, Depends(get_session)]