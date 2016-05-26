# coding=utf-8
from sqlalchemy import Column, Integer, String, Text
from .model import Model

class User(Model):
    __tablename__ = "user"

    owner_id = Column(Integer(), primary_key=True)
    user_name = Column(String(45))
    user_description = Column(Text())

    def __init__(self):
        Model.__init__(self)