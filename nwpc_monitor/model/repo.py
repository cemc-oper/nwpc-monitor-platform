# coding=utf-8
from sqlalchemy import Column, Integer, String, Text
from .model import Model

class Repo(Model):
    __tablename__ = "repo"

    repo_id = Column(Integer(), primary_key=True)
    owner_id = Column(Integer())
    repo_name = Column(String(45))
    repo_type = Column(String(10)) # [sms]
    repo_description = Column(Text())

    def __init__(self):
        Model.__init__(self)