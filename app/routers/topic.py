from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema, TokenData
from app.services.topic import TopicService

topicRouter: Blueprint = Blueprint('topicController', __name__, url_prefix="/topics")
