"""
* Project Name: AWF-FinalProject
* File Name: test_authentication.py
* Programmer: Philip Arff
* Date: Tue, Apr 20, 2021
* Description: This tests the user authentication
"""


def test_login(client, db, mocker):
    # Arrange
    expected_token = "xxxxx.yyyyy.zzzzz"
    mocker.patch("main.issue_jwt_token", new=lambda _: expected_token)

    # Act
    response = client.post(
        "/api/login", json={"username": "alice", "password": "simple_password"}
    )

    # Assert
    assert response.status_code == 200
    assert response.json() == expected_token


def test_get_user_valid_auth(client):
    """ Calls the get user route with a valid auth token. """
    # Arrange
    user_id = 1
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.RAuDG1t4uERT9Za3P4MzvLiUYAv3dtyHQBp4N45MhhA"

    # Act
    response = client.get(f"api/users/{user_id}", headers={"auth-token": token})

    # Assert
    assert response.status_code == 200


def test_get_user_bad_auth(client):
    """ Calls the get user route with an invalid auth token. """
    # Arrange
    user_id = 1
    token = "bad_token"

    # Act
    response = client.get(f"api/users/{user_id}", headers={"auth-token": token})

    # Assert
    assert response.status_code in [401, 403]


def test_del_valid_auth(client):
    """ Calls the get user route with a valid auth token. """
    # Arrange
    user_id = 1
    token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VyX2lkIjoxfQ.RAuDG1t4uERT9Za3P4MzvLiUYAv3dtyHQBp4N45MhhA"

    # Act
    response = client.get(f"api/users/{user_id}", headers={"auth-token": token})

    # Assert
    assert response.status_code == 200
