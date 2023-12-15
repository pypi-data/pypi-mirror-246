import logging

# Порт поумолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777
# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'
# Максимальная очередь подключений
MAX_CONNECTIONS = 5
# Максимальная длинна сообщения в байтах
MAX_PACKAGE_LENGTH = 1024
# Кодировка проекта
ENCODING = 'utf-8'
# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
RECEIVER = 'to'
PUBLIC_KEY = 'pubkey'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
RESPONSE = 'response'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'mess_text'
EXIT = 'exit'
BIN = 'bin'

# Словари - ответы:
RESPONSE_200 = {RESPONSE: 200}
RESPONSE_202 = {RESPONSE: 202}
RESPONSE_400 = {
            RESPONSE: 400,
            ERROR: None
        }
RESPONSE_205 = {
    RESPONSE: 205
}

RESPONSE_511 = {
    RESPONSE: 511,
    BIN: None
}

ADD_CONTACT = 'add_contact'
DEL_CONTACT = 'del_contact'
GET_CONTACTS = 'get_contacts'
GET_USERS = 'get_users'
CONTACT = 'contact'
DATA = 'data'
GET_PUBLIC_KEY = 'pubkey_need'


