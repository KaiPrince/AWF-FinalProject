"""
* Project Name: AWF-FinalProject
* File Name: test_users_api.py
* Programmer: Kai Prince
* Date: Tue, Apr 20, 2021
* Description: This file contains tests for our users api.
"""
import pytest
from pytest_mock import MockFixture
from sqlalchemy import text


def test_list_users(client, db):
    """ Gets a list of all users. """
    # Arrange

    # Act
    response = client.get("/api/users")

    # Assert
    assert response.status_code == 200
    assert response.json() == {
        "users": [
            {"user_id": 1, "username": "alice"},
            {"user_id": 2, "username": "bob"},
        ]
    }


def test_get_user(client):
    """ Gets a user by id. """
    # Arrange
    alice_data = {"user_id": 1, "username": "alice"}
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.RAuDG1t4uERT9Za3P4MzvLiUYAv3dtyHQBp4N45MhhA"

    # Act
    response = client.get("/api/users/1", headers={"auth-token": token})

    # Assert
    assert response.status_code == 200
    assert response.json() == alice_data


def test_create_user(client, db, mocker: MockFixture):
    """ Create a new user. """
    # Arrange
    username = "charlie"
    password = "finger_biter"

    expected_salt = b"\xa8\xce\x99\xad\x8f\xab\xd9\x96\xdd\xb9k\x160\x82\x84t"
    mocker.patch("crypto.generate_salt", new=lambda: expected_salt)
    expected_hash = b"\xa3\xdf\xec\x7f\xba-~\xb7\x9a\x8c\xf7\xe4\x87\xbcOI\xa2$\x02\xcb\xc7\xf2nj@\x14\xa5\x93d\xd5\x15\x93"

    # Act
    response = client.post(
        "/api/users/new", json={"username": username, "password": password}
    )

    # Assert
    assert response.status_code in [200, 201]

    with db.connect() as connection:
        query_result = connection.execute(
            text("Select user_id, username, hash, salt From account"),
        )
        db_users = [
            {
                "user_id": row["user_id"],
                "username": row["username"],
                "hash": row["hash"],
                "salt": row["salt"],
            }
            for row in query_result
        ]
    assert username in [x["username"] for x in db_users]
    assert {
        "user_id": 3,
        "username": username,
        "hash": expected_hash,
        "salt": expected_salt,
    } in db_users


def test_update_user(client, db, mocker):
    """ Change the user's password. """
    # Arrange
    user_id = 1
    password = "finger_biter"

    expected_salt = b"\xa8\xce\x99\xad\x8f\xab\xd9\x96\xdd\xb9k\x160\x82\x84t"
    mocker.patch("crypto.generate_salt", new=lambda: expected_salt)
    expected_hash = b"\xa3\xdf\xec\x7f\xba-~\xb7\x9a\x8c\xf7\xe4\x87\xbcOI\xa2$\x02\xcb\xc7\xf2nj@\x14\xa5\x93d\xd5\x15\x93"

    # Act
    response = client.put(
        f"/api/users/{user_id}", json={"username": "alice", "password": password}
    )

    # Assert
    assert response.status_code == 200

    with db.connect() as connection:
        query_result = connection.execute(
            text("Select hash, salt From account Where user_id = :user_id"),
            {"user_id": user_id},
        )
        db_users = [
            {
                "hash": row["hash"],
                "salt": row["salt"],
            }
            for row in query_result
        ]
    assert len(db_users) == 1
    user_hash = db_users[0]["hash"]
    user_salt = db_users[0]["salt"]

    assert user_hash == expected_hash
    assert user_salt == expected_salt


def test_delete_user(client, db):
    """ Delete a user by id. """
    # Arrange
    user_id = 1

    # Act
    response = client.delete(f"/api/users/{user_id}")

    # Assert
    assert response.status_code in [200, 204]
    with db.connect() as connection:
        cursor = connection.execute(
            text("Select user_id, username, hash, salt From account"),
        )
        user_ids = [row["user_id"] for row in cursor]
    assert user_id not in user_ids
