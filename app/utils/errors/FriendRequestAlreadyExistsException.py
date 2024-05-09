from app.utils.errors.GException import GException


class FriendRequestAlreadyExistsException(GException):
    message = "This user is already a friend of yours or has requested your friendship"
    code = 409