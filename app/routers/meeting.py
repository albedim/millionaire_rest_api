from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.schema.schema import UserAuthSchema, UserRefreshSchema, UserCompleteSchema, UserSigninSchema, TokenData
from app.services.meeting import MeetingService

meetingRouter: Blueprint = Blueprint('meetingController', __name__, url_prefix="/meetings")
