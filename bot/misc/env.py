from os import environ
from typing import Final

class TgKeys:
    TOKEN: Final = environ.get('TOKEN', 'your token!')
    ADMIN_TOKEN: Final = environ.get('ADMIN_TOKEN', 'your token!')

class dbKeys:
    host: Final = environ.get('host', 'your host!')
    user: Final = environ.get('user', 'your user!')
    password: Final = environ.get('password', 'your password!')
    db_name: Final = environ.get('db_name', 'your db_name!')