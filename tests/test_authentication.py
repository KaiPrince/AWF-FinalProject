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
