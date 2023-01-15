from contextvars import ContextVar

import peewee
from peewee import *

DATABASE_NAME = "test.db"

db_state_default = {"closed": None, "conn": None, "ctx": None, "transactions": None}
db_state = ContextVar("db_state", default=db_state_default.copy())


class PeeweeConnectionState(peewee._ConnectionState):
    def __init__(self, **kwargs):
        super().__setattr__("_state", db_state)
        super().__init__(**kwargs)

    def __setattr__(self, name, value):
        self._state.get()[name] = value

    def __getattr__(self, name):
        return self._state.get()[name]


mysql_db = MySQLDatabase('micro', user='root', password='121133', host='localhost', port=3306)
mysql_db._state = PeeweeConnectionState()
