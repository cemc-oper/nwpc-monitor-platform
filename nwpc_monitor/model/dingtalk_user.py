# coding=utf-8
from sqlalchemy import Column, Integer, String, Text
from .model import Model

class DingtalkUser(Model):
    __tablename__ = "dingtalk_user"

    dingtalk_user_id = Column(Integer(), primary_key=True)
    user_id = Column(Integer())
    dingtalk_member_userid = Column(Text())

    def __init__(self):
        Model.__init__(self)