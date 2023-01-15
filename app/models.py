import peewee

from .data import mysql_db


class Book(peewee.Model):
    title = peewee.CharField()
    body = peewee.CharField()

    class Meta:
        database = mysql_db
