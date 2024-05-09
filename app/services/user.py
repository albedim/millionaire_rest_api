from datetime import timedelta
import jwt
from flask_jwt_extended import create_access_token
from app.model.repository.user import UserRepository
from app.utils.errors.EmailNotSentException import EmailNotSentException
from app.utils.errors.GException import GException
from app.utils.errors.InvalidSchemaException import InvalidSchemaException
from app.utils.errors.TokenExpiredException import TokenExpiredException
from app.utils.errors.UnAuthotizedException import UnAuthorizedException
from app.utils.errors.UnMatchedPasswordException import UnMatchedPasswordException
from app.utils.errors.UserAlreadyExistsException import UserAlreadyExistsException
from app.utils.errors.UserNotFoundException import UserNotFoundException
from app.utils.schema import WELCOME_EMAIL, RECOVER_PASSWORD_EMAIL
from app.utils.utils import createSuccessResponse, createErrorResponse, hashString, send_html_email, \
    getEmails, BASE_FE_URL


class UserService:

    @classmethod
    def getUser(cls, auth, userId):
        try:
            authUser = UserRepository.getUserById(auth['user_id'])
            if authUser is None:
                raise UnAuthorizedException()

            user = UserRepository.getUserById(userId)
            if user is None:
                raise UserNotFoundException()

            isFriend = FriendRepository.get(user.user_id, authUser.user_id) is not None
            isFriendRequestOpen = (
                    FriendRequestRepository.get(user.user_id, authUser.user_id) is not None or
                    FriendRequestRepository.get(authUser.user_id, user.user_id) is not None
            )

            return createSuccessResponse(
                    user.toJSON(
                        friend={
                            "friendable": not isFriend and not isFriendRequestOpen,
                            "is_request_pending": isFriendRequestOpen
                        },
                        own=authUser.user_id == user.user_id
                    )
            )
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def signin(cls, request):
        try:
            user = UserRepository.getUserByEmail(request['email'])

            if user is None:
                raise UserNotFoundException()
            if user.password == hashString(request['password']):
                return createSuccessResponse({
                    'token': create_access_token(identity={'user_id': user.user_id, 'expires_in': 14}, expires_delta=timedelta(days=14)),
                    'expires_in': 14
                })
            else:
                raise UserNotFoundException()

        except UserNotFoundException as exc:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException(exc))

    @classmethod
    def sync(cls, tokenSub):
        try:
            user = UserRepository.getUserById(tokenSub['user_id'])
            if user is None:
                raise UserNotFoundException()
            return createSuccessResponse(True)
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException())
        except jwt.exceptions.ExpiredSignatureError:
            return createErrorResponse(TokenExpiredException())
        except jwt.exceptions.DecodeError:
            return createErrorResponse(UnAuthorizedException())
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException(exc))

    @classmethod
    def signup(cls, request):
        try:
            user = UserRepository.getUserByEmail(request['email'])

            if user is not None:
                raise UserAlreadyExistsException()

            user = UserRepository.create(
                request['email'],
                request['anonymous_name'],
                None if request['bio'] == "" else request['bio'],
                hashString(request['password'])
            )

            send_html_email(request['email'], getEmails("welcome")['title'],
                            WELCOME_EMAIL.replace("{anonymous_name}", user.anonymous_name)
                            .replace("{BASE_FE_URL}", BASE_FE_URL))
            return createSuccessResponse({
                'token': create_access_token(identity={'user_id': user.user_id},
                                             expires_delta=timedelta(days=14)),
                'expires_in': 14
            })

        except UserAlreadyExistsException as exc:
            return createErrorResponse(UserAlreadyExistsException)
        except KeyError as exc:
            return createErrorResponse(InvalidSchemaException)
        except Exception as exc:
            print(exc)
            return createErrorResponse(GException(exc))

    @classmethod
    def getMatchingUsers(cls, auth, name):
        try:
            user = UserRepository.getUserById(auth['user_id'])
            if user is None:
                raise UserNotFoundException

            users = UserRepository.getUsers(user.user_id, name)
            res = []
            for user in users:
                res.append(user.toJSON())
            return createSuccessResponse(res)
        except UserNotFoundException:
            return createErrorResponse(UnAuthorizedException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def change(cls, auth, request):
        try:
            userId = auth['user_id']
            user = UserRepository.getUserById(userId)

            if user is None:
                raise UserNotFoundException()

            password = hashString(request['password']) if request['password'] != "" else hashString(user.password)
            bio = request['bio'] if request['bio'] != "" else None
            UserRepository.change(user, bio, password)

            return createSuccessResponse("changed")
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def recover(cls, request):
        try:
            user = UserRepository.getUserByEmail(request['email'])

            if user is None:
                raise UserNotFoundException()

            recoveryToken = UserRepository.createRecoveryToken(user)
            send_html_email(user.email, getEmails("recover_password")['title'],
                        RECOVER_PASSWORD_EMAIL.replace("{anonymous_name}", user.anonymous_name)
                        .replace("{RECOVER_PASSWORD_URL}", f"{BASE_FE_URL}/create_password?token={recoveryToken}"))
            return createSuccessResponse("An email to recover your password was sent to you")

        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except EmailNotSentException:
            return createErrorResponse(EmailNotSentException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

    @classmethod
    def createPassword(cls, request):
        try:
            user = UserRepository.getUserByRecoveryToken(request['recovery_token'])

            if user is None:
                raise UserNotFoundException()

            if request['password'] != request['confirm_password']:
                raise UnMatchedPasswordException()

            UserRepository.createPassword(user, hashString(request['password']))
            return createSuccessResponse("created")
        except UserNotFoundException:
            return createErrorResponse(UserNotFoundException)
        except UnMatchedPasswordException:
            return createErrorResponse(UnMatchedPasswordException)
        except Exception as exc:
            return createErrorResponse(GException(exc))

