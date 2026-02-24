from typing import Optional, List
from .base import BaseBitrixModel
from pydantic import Field


class ContactPhone(BaseBitrixModel):
    id: str = Field(..., alias="ID")
    value_type: str = Field(..., alias="VALUE_TYPE")
    value: str = Field(..., alias="VALUE")
    type_id: str = Field(..., alias="TYPE_ID")

class Contact(BaseBitrixModel):
    id: str = Field(alias="ID")
    name: str = Field(alias="NAME")
    last_name: Optional[str] = Field(None, alias="LAST_NAME")
    second_name: Optional[str] = Field(None, alias="SECOND_NAME")
    assigned_by_id: str = Field(alias="ASSIGNED_BY_ID")
    phones: List[ContactPhone] = Field(default_factory=list, alias="PHONE")

class ContactResponse(BaseBitrixModel):
    result: Contact