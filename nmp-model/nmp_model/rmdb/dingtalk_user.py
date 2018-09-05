# coding=utf-8
from sqlalchemy import Column, Integer, Text, ForeignKey
from .model import Model
from .user import User


class DingtalkUser(Model):
    __tablename__ = "dingtalk_user"

    dingtalk_user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey(User.owner_id), nullable=False)
    dingtalk_member_userid = Column(Text, nullable=False)

    def __init__(self):
        Model.__init__(self)
