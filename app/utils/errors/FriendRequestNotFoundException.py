from app.utils.errors.GException import GException


class FriendRequestNotFoundException(GException):
    message = "Friend request was not found"
    code = 404