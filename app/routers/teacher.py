from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema, TokenData
from app.services.teacher import TeacherService

teacherRouter: Blueprint = Blueprint('teacherController', __name__, url_prefix="/teachers")
