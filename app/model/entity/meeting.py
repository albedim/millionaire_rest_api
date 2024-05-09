import datetime

from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class Meeting(sql.Model):
    __tablename__ = "meetings"
    meeting_id = sql.Column(sql.Integer, primary_key=True)
    title = sql.Column(sql.String(64), nullable=False)
    topic_id = sql.Column(sql.Integer, sql.ForeignKey("topics.topic_id"), nullable=False)
    teacher_id = sql.Column(sql.Integer, sql.ForeignKey("teachers.teacher_id"), nullable=False)
    user_id = sql.Column(sql.String(4), sql.ForeignKey("users.user_id"), nullable=False)
    created_on = sql.Column(sql.DateTime, nullable=False)

    def __init__(self, title, topic_id, teacher_id, user_id):
        self.title = title
        self.topic_id = topic_id
        self.teacher_id = teacher_id
        self.user_id = user_id
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