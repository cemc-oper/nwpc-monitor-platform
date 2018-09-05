# coding=utf-8
from sqlalchemy import Column, Integer, Text, DateTime, ForeignKey
from .model import Model
from .repo import Repo
from .dingtalk_user import DingtalkUser


class DingtalkWarnWatch(Model):
    __tablename__ = "dingtalk_warn_watch"

    id = Column(Integer, primary_key=True, autoincrement=True)
    repo_id = Column(Integer, ForeignKey(Repo.repo_id), nullable=False)
    dingtalk_user_id = Column(Integer, ForeignKey(DingtalkUser.dingtalk_user_id), nullable=False)
    start_date_time = Column(DateTime, default=None)
    end_date_time = Column(DateTime, default=None)

    def __init__(self):
        Model.__init__(self)
