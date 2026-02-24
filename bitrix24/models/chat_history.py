from typing import Dict
from .base import BaseBitrixModel
from pydantic import Field


class Message(BaseBitrixModel):
    id: str
    chat_id: str = Field(alias="chatid")
    sender_id: str = Field(alias="senderid")
    recipient_id: str = Field(alias="recipientid")
    date: str
    text: str

class ChatUser(BaseBitrixModel):
    id: str
    name: str
    bot: bool
    active: bool
    first_name: str = Field(alias="firstName")
    last_name: str = Field(alias="lastName")
    external_auth_id: str = Field(alias="externalAuthId")
    extranet: bool

    @property
    def role(self) -> str:

        """Определяет роль пользователя в открытой линии"""
        if self.bot:
            return "bot"
        if self.extranet or self.external_auth_id == "imconnector":
            return "client"
        return "operator"

class ChatHistoryResult(BaseBitrixModel):
    message: Dict[str, Message]
    users: Dict[str, ChatUser]

class ChatHistoryResponse(BaseBitrixModel):
    result: ChatHistoryResult