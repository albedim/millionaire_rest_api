import datetime
from sqlalchemy import text, desc
from sqlalchemy.orm import aliased
from app.configuration.config import sql
from app.model.entity.user import User
from app.utils.utils import generateUuid


class UserRepository:

    @classmethod
    def create(cls, email, name, password):
        user: User = User(name, password, password)
        sql.session.add(user)
        sql.session.commit()
        return user

    @classmethod
    def getUserByEmail(cls, email):
        user = sql.session.query(User).filter(User.email == email).first()
        return user

    @classmethod
    def getUserById(cls, user_id):
        user = sql.session.query(User).filter(User.user_id == user_id).first()
        return user

    @classmethod
    def setStoryLimit(cls, user):
        user.available_stories -= 1
        sql.session.commit()
        return user

    @classmethod
    def resetStoryLimit(cls, user):
        user.available_stories += 10
        user.as_limit_date = None
        sql.session.commit()
        return user

    @classmethod
    def setStoryLimitDate(cls, user):
        user.as_limit_date = datetime.date.today() + datetime.timedelta(days=1)
        sql.session.commit()
        return user


    @classmethod
    def signin(cls, email, password):
        user = sql.session.query(User).filter(User.email == email).filter(User.password == password).first()
        return user

    @classmethod
    def getFriends(cls, userId):
        friends = sql.session.query(User, text("friends.created_on"))\
                   .join(Friend, Friend.friend_id == User.user_id)\
                   .filter(Friend.user_id == userId).order_by(desc(Friend.created_on)).all()
        return friends

    @classmethod
    def getSentFriendRequests(cls, userId):
        friendRequests = sql.session.query(User, text("friendrequests.created_on")) \
            .join(FriendRequest, FriendRequest.target_id == User.user_id) \
            .filter(FriendRequest.user_id == userId).order_by(desc(FriendRequest.created_on)).all()
        return friendRequests

    @classmethod
    def getReceivedFriendRequests(cls, userId):
        friendRequests = sql.session.query(User, text("friendrequests.created_on")) \
            .join(FriendRequest, FriendRequest.user_id == User.user_id) \
            .filter(FriendRequest.target_id == userId).order_by(desc(FriendRequest.created_on)).all()
        return friendRequests

    @classmethod
    def getUsers(cls, userId, name):
        f1 = aliased(Friend)
        f2 = aliased(Friend)

        users = (
            sql.session.query(User)
            .outerjoin(f1, (User.user_id == f1.friend_id) & (f1.user_id == userId))
            .outerjoin(f2, (User.user_id == f2.user_id) & (f2.friend_id == userId))
            .filter(User.user_id != userId)
            .filter(f1.friend_id.is_(None))
            .filter(f2.user_id.is_(None))
            .filter(User.anonymous_name.like(f'%{name}%'))
            .all()
        )
        return users

    @classmethod
    def change(cls, user, bio, password):
        user.bio = bio
        user.password = password
        sql.session.commit()

    @classmethod
    def createRecoveryToken(cls, user):
        recoveryToken = generateUuid(size=18).replace("-", "")
        user.recovery_token = recoveryToken
        sql.session.commit()
        return recoveryToken

    @classmethod
    def getUserByRecoveryToken(cls, recoveryToken):
        user = sql.session.query(User).filter(User.recovery_token == recoveryToken).first()
        return user

    @classmethod
    def createPassword(cls, user, password):
        user.password = password
        user.recovery_token = None
        sql.session.commit()