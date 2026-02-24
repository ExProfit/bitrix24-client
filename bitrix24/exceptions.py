class BitrixAPIError(Exception):
    """Исключение для ошибок Bitrix API"""
    def __init__(self, message, status_code=None, response_data=None):
        self.status_code = status_code
        self.response_data = response_data
        super().__init__(message)