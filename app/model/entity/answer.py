import datetime
from sqlalchemy import String, Column, Date, Boolean, DateTime
from app.configuration.config import sql
from app.utils.utils import generateUuid, BASE_URL


class Answer(sql.Model):
    __tablename__ = "answers"
    answer_id = sql.Column(sql.Integer, primary_key=True)
    content = sql.Column(sql.String(500), nullable=False)
    question_id = sql.Column(sql.Integer, sql.ForeignKey("questions.question_id"), nullable=False)
    meeting_id = sql.Column(sql.Integer, sql.ForeignKey("meetings.meeting_id"), nullable=False)

    def __init__(self, content, question_id, meeting_id):
        self.content = content
        self.question_id = question_id
        self.meeting_id = meeting_id

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