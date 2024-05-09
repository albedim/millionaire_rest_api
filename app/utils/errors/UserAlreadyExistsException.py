from app.utils.errors.GException import GException


class UserAlreadyExistsException(GException):
    message = "User already exists"
    code = 409