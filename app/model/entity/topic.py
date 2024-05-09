import datetime

from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class Topic(sql.Model):
    __tablename__ = "topics"
    topic_id = sql.Column(sql.Integer, primary_key=True)
    name = sql.Column(sql.String(24), nullable=False)
    premium = sql.Column(sql.Boolean, nullable=False)
    name_id = sql.Column(sql.String(24), nullable=False)

    def __init__(self):
        ...

    def toJSON(self, **kvargs):
        obj = {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'password': self.password,
            'created_on': str(self.created_on)
        }
        for kvarg in kvargs:
            obj[kvarg] = kvargs[kvarg]
        return obj