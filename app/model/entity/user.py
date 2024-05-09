import datetime

from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class User(sql.Model):
    __tablename__ = "users"
    user_id = sql.Column(sql.String(4), primary_key=True)
    email = sql.Column(sql.String(64), nullable=False)
    password = sql.Column(sql.String(64), nullable=False)
    name = sql.Column(sql.String(24), nullable=False)
    created_on = sql.Column(sql.Date, nullable=False)

    def __init__(self, name, password, email):
        self.user_id = generateUuid(size=4)
        self.email = email
        self.name = name
        self.password = password
        self.created_on = datetime.datetime.utcnow()

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