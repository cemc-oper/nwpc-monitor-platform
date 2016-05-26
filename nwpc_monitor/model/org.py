# coding=utf-8
from sqlalchemy import Column, Integer, String, Text
from .model import Model

class Org(Model):
    __tablename__ = "org"

    owner_id = Column(Integer(), primary_key=True)
    org_name = Column(String(45))
    org_description = Column(Text())

    def __init__(self):
        Model.__init__(self)