"""Bitrix24 API Client"""

from .api import BitrixAPI
from .exceptions import BitrixAPIError
from .models import (
    BaseBitrixModel,
    User, UsersResponse,
    Contact, ContactResponse,
    Deal, DealResponse,
    Chat, ChatResponse,
    Dialog, DialogResponse,
    ChatUser, ChatHistoryResponse, ChatHistoryResult, Message,
    Category, CategoryResponse
)

__version__ = "0.1.0"
__all__ = [
    "BitrixAPI",
    "BitrixAPIError",
    "BaseBitrixModel",
    "User", "UsersResponse",
    "Contact", "ContactResponse",
    "Deal", "DealResponse",
    "Chat", "ChatResponse",
    "Dialog", "DialogResponse",
    "ChatUser", "ChatHistoryResponse", "ChatHistoryResult", "Message",
    "Category", "CategoryResponse",
]