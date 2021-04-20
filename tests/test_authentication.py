"""
* Project Name: AWF-FinalProject
* File Name: test_authentication.py
* Programmer: Philip Arff
* Date: Tue, Apr 20, 2021
* Description: This tests the user authentication
"""


def test_login(client, db):
    response = client.post(
        "/api/login", json={"username": "alice", "password": "simple_password"}
    )
    assert response.status_code == 200
