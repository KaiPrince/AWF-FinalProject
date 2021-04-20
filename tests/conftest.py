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
        {"username": "alice", "password": "simple_password"},
        {"username": "bob", "password": "P@ssw0rd!"},
    ]

    sql = text(
        "INSERT INTO account (username, hash, salt) VALUES(:username, :password_hash, :salt)"
    )

    with engine.connect() as connection:

        for statement in init_script.split(";"):
            connection.execute(statement)

        for user in users:
            salt, password_hash = salt_hash_password(user["password"])
            username = user["username"]
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
