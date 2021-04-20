"""
* Project Name: AWF-FinalProject
* File Name: conftest.py
* Programmer: Kai Prince
* Date: Tue, Apr 20, 2021
* Description: This file contains config for testing.
"""
from pathlib import Path

import pytest
from fastapi import FastAPI, Depends
from fastapi.testclient import TestClient
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

from crypto import make_salt_hash, salt_hash_password
from db import get_db, get_connection_string
from main import app as _app
from models import Credentials

SQLALCHEMY_DATABASE_URL = "sqlite:///./tests/db.db"
INIT_SCRIPT = "./tests/db.sql"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_mock_db():
    try:
        db = session_local()
        yield db
    finally:
        db.close()


@pytest.fixture
def app():

    _app.dependency_overrides[get_db] = get_mock_db

    init_script = Path(INIT_SCRIPT).read_text()
    users = [
        {
            "username": "alice",
            "password": "simple_password",
            "salt": b"`\x98\xe3\xd3,`Pq\xef\xd6'\x1c}\x9c\x99B",
            "hash": b"\x9fG&\xfe\xe0x[\x8d<\xcdc\x1b\x91\xddw\x06\x94O\x8cl\xe6\xb3~\x84;8PE$\xccj\x1f",
        },
        {
            "username": "bob",
            "password": "P@ssw0rd!",
            "salt": b"\xd6\xf2?!\x84\r6z\xd0\xe2n\xdd\x82\t\x7f\xfe",
            "hash": b'\xa1"\x8b\x1a\xeb\xcc[j,u\x91\xc30\x1c\x9e\x1e\xed\x16\x9b\xfb\x0b\xd8#\x9c!\x86,\x12\xdd>\xb8]',
        },
    ]

    sql = text(
        "INSERT INTO account (username, hash, salt) VALUES(:username, :password_hash, :salt)"
    )

    with engine.connect() as connection:

        for statement in init_script.split(";"):
            connection.execute(statement)

        for user in users:
            username = user["username"]
            salt = user["salt"]
            password_hash = user["hash"]
            connection.execute(
                sql,
                {"username": username, "password_hash": password_hash, "salt": salt},
            )

    yield _app


@pytest.fixture
def client(app):
    with TestClient(app) as client:
        yield client


@pytest.fixture
def db(app):
    return engine
