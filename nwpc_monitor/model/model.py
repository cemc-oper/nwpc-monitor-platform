# coding=utf-8
from sqlalchemy.ext.declarative import declarative_base


ModelBase = declarative_base()

class Model(ModelBase):

    def __init__(self):
        pass

    def columns(self):
        return [c.name for c in self.__table__.columns]

    def to_dict(self):
        return dict([(c, getattr(self, c)) for c in self.columns()])