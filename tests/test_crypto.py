"""
* Project Name: AWF-FinalProject
* File Name: test_crypto.py
* Programmer: Philip Arff
* Date: Tue, Apr 20, 2021
* Description: This tests the crypto module
"""

import pytest
from crypto import salt_hash_password, validate_password


@pytest.mark.parametrize("password", ["simple_password", "ASF2@!askgf:;"])
def test_can_salt_hash_password(password):
    """ Test the crypto functionality """
    # Act
    salt, password_hash = salt_hash_password(password)

    # Assert
    assert validate_password(salt, password_hash, password)
