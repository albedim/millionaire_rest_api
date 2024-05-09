from app.configuration.config import sql
from app.model.entity.topic import Topic

class TopicRepository:

    @classmethod
    def getTopics(cls):
        topics = sql.session.query(Topic).from_statement(
            text("SELECT * "
                 "FROM topics "
                 "JOIN meetings ON meetings.topic_id = topics.topic_id "
                 "JOIN answers ON answers.meeting_id = meetings.meeting_id "
                 "GROUP BY answers.question_id "
                 "WHERE meetings.user_id = :userId")
        )