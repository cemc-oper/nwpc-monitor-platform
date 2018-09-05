# coding=utf-8
from sqlalchemy import Column, Integer, String, Text, Index, ForeignKey
from .model import Model
from .owner import Owner


class User(Model):
    __tablename__ = "user"

    owner_id = Column(Integer, ForeignKey(Owner.owner_id), primary_key=True)
    user_name = Column(String(45), nullable=False)
    user_description = Column(Text)

    index_user_name = Index(user_name, unique=True)

    def __init__(self):
        Model.__init__(self)
