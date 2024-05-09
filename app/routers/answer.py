from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema, TokenData
from app.services.answer import AnswerService

answerRouter: Blueprint = Blueprint('answerController', __name__, url_prefix="/answers")
