# coding=utf-8
from sqlalchemy import Column, Integer, String, Index, ForeignKey
from .model import Model
from .org import Org
from .user import User


class OrgUser(Model):
    __tablename__ = "org_user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    org_id = Column(Integer, ForeignKey(Org.owner_id), nullable=False)
    user_id = Column(Integer, ForeignKey(User.owner_id), nullable=False)
    relationship = Column(String(20), nullable=False) # [member, watcher]

    index_org_user = Index("index_org_user", org_id, user_id, unique=True)

    def __init__(self):
        Model.__init__(self)
