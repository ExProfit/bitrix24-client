import json
from httpx import Client
from typing import Optional, Union
from loguru import logger
from .exceptions import BitrixAPIError
from .utils import RateLimiter
from .models import (
    UsersResponse, ContactResponse, DealResponse, DealListResponse,
    ChatResponse, DialogResponse, ChatHistoryResponse, CategoryResponse
)



class BitrixAPI:

    def __init__(self, webhook_url, verify: bool = True, timeout: float = 30.0, requests_per_second=2):
        self.session = Client(timeout=timeout, verify=verify)
        self.webhook_url = webhook_url
        self.rate_limiter = RateLimiter(requests_per_second)

    def _request(self, method, params=None):
        self.rate_limiter.wait()
        url = self.webhook_url + method
        if params is None:
            params = {}

        logger.debug(f"→ Bitrix API: {method} | {json.dumps(params, ensure_ascii=False)}")

        try:
            response = self.session.post(url, json=params)
            logger.debug(f"← Bitrix API: {method} | {response.status_code} | {response.text[:200]}")

            # Проверяем HTTP статус
            response.raise_for_status()
            
            # Пытаемся распарсить JSON
            try:
                result = response.json()
            except ValueError as e:
                raise BitrixAPIError(
                    f"Invalid JSON response: {response.text[:200]}",
                    response.status_code
                ) from e
            
            # Проверяем, есть ли ошибка в ответе Bitrix
            if 'error' in result:
                error_desc = result.get('error_description', 'No description')
                raise BitrixAPIError(
                    f"Bitrix API error: {result['error']} - {error_desc}",
                    response.status_code,
                    result
                )
                
            return result
        
        except Exception as e:
            logger.error(f"Ошибка Bitrix API: {method} | {str(e)}")
            raise  # Пробрасываем исключение дальше для обработки в основном коде


    def get_call_list(self, start: int, params: dict):
        method = 'voximplant.statistic.get'
        if params is None:
            params = {}
        if start:
            params['start'] = start
        return self._request(method, params=params)

    def get_file_from_disk(self, file_id: int):
        method = 'disk.file.get'
        params = {'id': file_id}
        return self._request(method, params=params)
    
    def get_chats_openline(self):
        method = 'imopenlines.config.list.get'
        return self._request(method)

    # ==================== ВОРОНКИ ====================

    def get_category_list(self, entity_type_id: int, parse_response: bool = True):

        # получить список воронок
        method = 'crm.category.list'
        params = {'entityTypeId': entity_type_id}
        response = self._request(method, params)
    
        if parse_response:
            return CategoryResponse.model_validate(response)
        return response
    
    # ==================== СДЕЛКИ ====================

    def get_deal(self, deal_id, parse_response: bool = True):
        method = 'crm.deal.get'
        params = {'ID': deal_id}
        response = self._request(method, params)

        if parse_response:
            return DealResponse.model_validate(response)
        return response
    
    def get_deal_list(self, start=None, params=None, parse_response: bool = True):
        method = 'crm.deal.list'
        if params is None:
            params = {}
        if start:
            params['start'] = start
        response = self._request(method, params)

        if parse_response:
            return DealListResponse.model_validate(response)
        return response
    
    # ==================== ЛИДЫ ====================

    
    # ==================== КОНТАКТЫ ====================

    def get_contact(self, contact_id, parse_response: bool = True):
        method = 'crm.contact.get'
        params = {'ID': contact_id}
        response = self._request(method, params)

        if parse_response:
            return ContactResponse.model_validate(response)
        return response
    
    # ==================== ПОЛЬЗОВАТЕЛИ ====================

    def get_user(self, start: Optional[int] = None, params=None, parse_response: bool = True):

        # получить список пользователей
        method = 'user.get'
        if params is None:
            params = {}
        if start:
            params['start'] = start
        response = self._request(method, params=params)

        if parse_response:
            return UsersResponse.model_validate(response)
        return response
    
    # ==================== ПОИСК ДУБЛЕЙ ====================

    def find_duplicate(self, type: str, values: list, entity_type: str = 'CONTACT', parse_response: bool = True):

        # поиск дублей контактов/лидов/компаний
        method = 'crm.duplicate.findbycomm'
        params = {'type': type, 'values': values}
        if entity_type:
            params['entity_type'] = entity_type
        
        return self._request(method, params=params)
    
    # ==================== УВЕДОМЛЕНИЯ ====================

    def send_notification(self, user_id, message, parse_response: bool = True):

        # отправка уведомления
        method = 'im.notify.system.add'
        params = {'USER_ID': user_id, 'MESSAGE': message}
        
        return self._request(method, params=params)
    
    # ==================== ОТКРЫТЫЕ ЛИНИИ ====================

    def get_chats(self, crm_entity: int, crm_entity_type: str, active_only: str = 'Y', parse_response: bool = True):

        # получить чаты лида или сделки
        method = 'imopenlines.crm.chat.get'
        params = {
            'CRM_ENTITY': crm_entity,
            'CRM_ENTITY_TYPE': crm_entity_type,
            'ACTIVE_ONLY': active_only
        }
        response = self._request(method, params)

        if parse_response:
            return ChatResponse.model_validate(response)
        return response
    
    def get_dialog(
            self,
            chat_id: Optional[Union[int, str]] = None,
            dialog_id: Optional[str] = None,
            session_id: Optional[Union[int, str]] = None,
            user_code: Optional[str] = None,
            parse_response: bool = True
        ):
        
        # получить диалог
        method = 'imopenlines.dialog.get'
        params = {}
        
        if chat_id is not None:
            params['CHAT_ID'] = int(chat_id)
        if dialog_id is not None:
            params['DIALOG_ID'] = dialog_id
        if session_id is not None:
            params['SESSION_ID'] = int(session_id)
        if user_code is not None:
            params['USER_CODE'] = user_code
            
        if not params:
            raise ValueError('Хотя бы один параметр должен быть передан: chat_id, dialog_id, session_id or user_code')
            
        response = self._request(method, params)

        if parse_response:
            return DialogResponse.model_validate(response)
        return response
    
    def get_history_session(
            self,
            chat_id: Union[int, str],
            session_id: Union[int, str],
            parse_response: bool = True):

        # получить сообщения чата и диалога
        method = 'imopenlines.session.history.get'
        params = {'CHAT_ID': int(chat_id), 'SESSION_ID': int(session_id)}
        response = self._request(method, params)

        if parse_response:
            return ChatHistoryResponse.model_validate(response)
        return response
    
    # ==================== УНИВЕРСАЛЬНЫЕ МЕТОДЫ ====================

    def get_crm_item(self, entity_type: str, item_id: int, select: Optional[list] = None, parse_response: bool = False):

        method = 'crm.item.get'
        params = {
            'entityTypeId': self._get_entity_type_id(entity_type),
            'id': item_id
        }
        if select:
            params['select'] = select

        params['useOriginalUfNames'] = 'Y'

        return self._request(method, params)


    def get_crm_item_list(self, entity_type: str, filter_params: Optional[dict] = None,
                      select: Optional[list] = None, order: Optional[dict] = None,
                      start: Optional[int] = 0,
                      parse_response: bool = False):
        
        method = 'crm.item.list'
        params = {
            'entityTypeId': self._get_entity_type_id(entity_type)
        }
        if filter_params:
            params['filter'] = filter_params
        if select:
            params['select'] = select
        if order:
            params['order'] = order
        if start is not None:
            params['start'] = start

        params['useOriginalUfNames'] = 'Y'

        return self._request(method, params)
    
    def _get_entity_type_id(self, entity_type: str) -> int:
        """Преобразует строковый тип сущности в числовой ID."""
        mapping = {
            'lead': 1,
            'deal': 2,
            'contact': 3,
            'company': 4,
        }

        if entity_type.startswith('custom_'):
            # Предполагаем, что после 'custom_' идет числовой ID кастомной сущности
            try:
                return int(entity_type.split('_', 1)[1])
            except (ValueError, IndexError):
                raise ValueError(f"Invalid custom entity type format: {entity_type}. Expected 'custom_<number>'.")

        entity_id = mapping.get(entity_type.lower())

        if entity_id is None:
            raise ValueError(f"Unknown entity type: {entity_type}")
        
        return entity_id
