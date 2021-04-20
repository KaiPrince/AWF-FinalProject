"""
* Project Name: AWF-FinalProject
* File Name: crypto.py
* Programmer: Philip Arff
* Date: Tue, Apr 20, 2021
* Description: Functions to salt/hash a password and validate a hashed password
"""


import hashlib
import hmac
import os

from models import Credentials


def generate_salt():
    return os.urandom(16)


def generate_hash(salt, password):
    return hashlib.pbkdf2_hmac("sha256", password.encode(), salt, 100000)


def salt_hash_password(password):
    salt = generate_salt()
    password_hash = generate_hash(salt, password)
    return salt, password_hash


def validate_password(salt, password_hash, attempt):
    return hmac.compare_digest(
        password_hash, hashlib.pbkdf2_hmac("sha256", attempt.encode(), salt, 100000)
    )


def make_salt_hash(credentials: Credentials):
    username = credentials.username
    password = credentials.password
    salt, password_hash = salt_hash_password(password)
    return username, password_hash, salt
