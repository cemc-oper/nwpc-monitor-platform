# coding=utf-8
from sqlalchemy import Column, BigInteger, String
from .model import Model

class Tickets64(Model):
    __tablename__ = "tickets_64"

    id = Column(BigInteger(), primary_key=True)
    stub = Column(String(45))
    owner_type = Column(String(1))

    def __init__(self):
        Model.__init__(self)