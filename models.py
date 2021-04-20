"""
* Project Name: AWF-FinalProject
* File Name: models.py
* Programmer: Kai Prince
* Date: Tue, Apr 20, 2021
* Description: This file contains model definitions.
"""


from typing import Optional

from pydantic import BaseModel


class Account(BaseModel):
    user_id: str
    username: str
    hash: str
    salt: str


class Credentials(BaseModel):
    username: str
    password: str
