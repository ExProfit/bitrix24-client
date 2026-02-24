from typing import List, Optional
from .base import BaseBitrixModel
from pydantic import Field


class Chat(BaseBitrixModel):
    chat_id: str = Field(alias="CHAT_ID")
    connector_id: str = Field(alias="CONNECTOR_ID")
    connector_title: str = Field(alias="CONNECTOR_TITLE")

class ChatResponse(BaseBitrixModel):
    result: List[Chat]

class Dialog(BaseBitrixModel):
    id: int
    dialog_id: Optional[str] = None
    entity_data_1: Optional[str] = None
    entity_type: Optional[str] = None
    name: Optional[str] = None
    owner: Optional[int] = None
    type: Optional[str] = None

class DialogResponse(BaseBitrixModel):
    result: Dialog