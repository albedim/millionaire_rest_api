import datetime

from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class Question(sql.Model):
    __tablename__ = "questions"
    question_id = sql.Column(sql.Integer, primary_key=True)
    topic_id = sql.Column(sql.Integer, nullable=False)
    content = sql.Column(sql.String(54), nullable=False)

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