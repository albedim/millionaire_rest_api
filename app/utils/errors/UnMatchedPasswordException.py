from app.utils.errors.GException import GException


class UnMatchedPasswordException(GException):
    message = "Passwords don't match"
    code = 400