from typing import Optional, List
from .base import BaseBitrixModel
from pydantic import Field


class Deal(BaseBitrixModel):
    id: str = Field(alias="ID")
    title: str = Field(alias="TITLE")
    type_id: Optional[str] = Field(None, alias="TYPE_ID")
    stage_id: Optional[str] = Field(None, alias="STAGE_ID")
    opportunity: Optional[str] = Field(None, alias="OPPORTUNITY")
    contact_id: Optional[str] = Field(None, alias="CONTACT_ID")
    category_id: Optional[str] = Field(None, alias="CATEGORY_ID")
    closed: Optional[str] = Field(None, alias="CLOSED")
    opened: Optional[str] = Field(None, alias="OPENED")
    assigned_by_id: Optional[str] = Field(None, alias="ASSIGNED_BY_ID")
    date_create: Optional[str] = Field(None, alias="DATE_CREATE")

class DealResponse(BaseBitrixModel):
    result: Deal

class DealListResponse(BaseBitrixModel):
    result: List[Deal]
    next: Optional[int] = None
    total: int