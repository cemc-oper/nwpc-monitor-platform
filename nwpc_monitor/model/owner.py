# coding=utf-8
from sqlalchemy import Column, Integer, String
from .model import Model

class Owner(Model):
    __tablename__ = "owner"

    owner_id = Column(Integer(), primary_key=True)
    owner_name = Column(String(45))
    owner_type = Column(String(10)) # [user, org]

    def __init__(self):
        Model.__init__(self)