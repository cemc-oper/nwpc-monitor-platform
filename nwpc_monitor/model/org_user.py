# coding=utf-8
from sqlalchemy import Column, Integer, String, Text
from .model import Model

class OrgUser(Model):
    __tablename__ = "org_user"

    id = Column(Integer(), primary_key=True)
    org_id = Column(Integer())
    user_id = Column(Integer())
    relationship = Column(String(20)) # [member, watcher]

    def __init__(self):
        Model.__init__(self)