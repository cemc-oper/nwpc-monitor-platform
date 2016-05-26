# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, DateTime
from .model import Model

class DingtalkWarnWatch(Model):
    __tablename__ = "dingtalk_warn_watch"

    id = Column(Integer(), primary_key=True)
    repo_id = Column(Integer())
    dingtalk_user_id = Column(Text())
    start_date_time = Column(DateTime(), default=None)
    end_date_time = Column(DateTime(), default=None)

    def __init__(self):
        Model.__init__(self)