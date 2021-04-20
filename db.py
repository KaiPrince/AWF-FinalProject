"""
* Project Name: AWF-FinalProject
* File Name: db.py
* Programmer: Kai Prince
* Date: Tue, Apr 20, 2021
* Description: This file contains database related functions.
"""
from fastapi import Depends
from sqlalchemy import create_engine, text

from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy.orm import sessionmaker

# TODO: Move database stuff to own file
# TODO: Move to .env
SQLALCHEMY_DATABASE_URL = "postgresql://Guest:Gu3stP@SS!@70.55.213.203/FinalProject"


# TODO: store in app session.


def get_connection_string():
    return SQLALCHEMY_DATABASE_URL


def get_db(connection_string: str = Depends(get_connection_string)):
    engine = create_engine(connection_string)
    session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    try:
        db = session_local()
        yield db
    finally:
        db.close()
