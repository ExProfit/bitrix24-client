from typing import Optional, List
from .base import BaseBitrixModel
from pydantic import Field

class User(BaseBitrixModel):
    id: str = Field(alias="ID")
    name: str = Field(alias="NAME")
    last_name: str = Field(alias="LAST_NAME")
    email: str = Field(alias="EMAIL")

class UsersResponse(BaseBitrixModel):
    result: List[User]
    total: Optional[int] = None
