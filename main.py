"""
* Project Name: AWF-FinalProject
* File Name: main.py
* Programmer: Kai Prince
* Date: Tue, Apr 20, 2021
* Description: This file contains the main entrypoint for the AWF FinalProject
*   backend.
"""
import os
from typing import Optional

from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from crypto import validate_password, make_salt_hash
from db import get_db
from models import Credentials
from philip_jwt import issue_jwt_token, decode_jwt

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/api/users/{user_id}")
def get_user(
    user_id: int, auth_token: Optional[str] = Header(None), db=Depends(get_db)
):

    token_payload = decode_jwt(auth_token)
    if auth_token is None or not token_payload:
        raise HTTPException(status_code=401, detail="Auth token invalid.")

    if token_payload["user_id"] != user_id:
        raise HTTPException(
            status_code=403, detail="User does not have permission for this action."
        )

    query = text("SELECT user_id, username FROM account WHERE user_id = :user_id")
    cursor = db.execute(query, {"user_id": user_id})

    results = [
        {"user_id": row["user_id"], "username": row["username"]} for row in cursor
    ]

    if len(results) > 1:
        raise HTTPException(status_code=500, detail="More than one user found.")

    if len(results) <= 0:
        raise HTTPException(status_code=500, detail="User not found.")

    return results[0]


@app.post("/api/users/new")
def create_account_route(credentials: Credentials, db=Depends(get_db)):
    username, password_hash, salt = make_salt_hash(credentials)

    sql = text(
        "INSERT INTO account (username, hash, salt) VALUES(:username, :password_hash, :salt)"
    )

    db.execute(
        sql, {"username": username, "password_hash": password_hash, "salt": salt}
    )
    db.commit()
    return "Success."


@app.post("/api/login")
def login_route(credentials: Credentials, db=Depends(get_db)):
    username = credentials.username
    password = credentials.password

    query = text("SELECT account.* FROM account WHERE account.username = :username")
    cursor = db.execute(query, {"username": username})

    results = [
        {
            "user_id": row["user_id"],
            "username": row["username"],
            "salt": row["salt"],
            "password_hash": row["hash"],
        }
        for row in cursor
    ]

    if len(results) > 1:
        raise HTTPException(status_code=500, detail="More than one user found.")

    if len(results) <= 0:
        raise HTTPException(status_code=500, detail="User not found.")

    user = results[0]
    if validate_password(user["salt"], user["password_hash"], password):
        payload = {"user_id": user["user_id"]}
        token = issue_jwt_token(payload)
        return token

    raise HTTPException(status_code=500, detail="Login failed")


@app.get("/api/users")
def list_users(db=Depends(get_db)):
    sql = text("SELECT user_id, username FROM account")
    result = db.execute(sql)
    users = [{"user_id": row["user_id"], "username": row["username"]} for row in result]

    return {"users": users}


@app.put("/api/users/{user_id}")
def update_password(
    user_id: int,
    credentials: Credentials,
    auth_token: Optional[str] = Header(None),
    db=Depends(get_db),
):
    token_payload = decode_jwt(auth_token)
    if auth_token is None or not token_payload:
        raise HTTPException(status_code=401, detail="Auth token invalid.")

    if token_payload["user_id"] != user_id:
        raise HTTPException(
            status_code=403, detail="User does not have permission for this action."
        )

    username, password_hash, salt = make_salt_hash(credentials)

    query = text(
        "UPDATE account SET hash = :hash, salt = :salt WHERE user_id = :user_id AND username = :username"
    )
    db.execute(
        query,
        {
            "user_id": user_id,
            "username": username,
            "hash": password_hash,
            "salt": salt,
        },
    )
    db.commit()

    return "Success."


@app.delete("/api/users/{user_id}")
def delete_user(
    user_id: int, auth_token: Optional[str] = Header(None), db=Depends(get_db)
):
    token_payload = decode_jwt(auth_token)
    if auth_token is None or not token_payload:
        raise HTTPException(status_code=401, detail="Auth token invalid.")

    if token_payload["user_id"] != user_id:
        raise HTTPException(
            status_code=403, detail="User does not have permission for this action."
        )

    sql = text("DELETE FROM account WHERE account.user_id = :user_id")
    db.execute(sql, {"user_id": user_id})
    db.commit()

    return "Success."
