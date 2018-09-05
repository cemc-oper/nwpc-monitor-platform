# coding=utf-8
from sqlalchemy import Column, BigInteger, CHAR
from .model import Model


class Tickets64(Model):
    __tablename__ = "tickets_64"

    id = Column(BigInteger, primary_key=True, nullable=False, autoincrement=True)
    stub = Column(CHAR(1))

    def __init__(self):
        Model.__init__(self)
