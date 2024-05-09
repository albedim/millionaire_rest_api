from app.utils.errors.GException import GException


class StoryNotFoundException(GException):
    message = "This story doesn't exist"
    code = 404