import base64
import hashlib
import json
from datetime import datetime
import jwt
import requests
import yaml
import string
import random
import uuid
from flask import jsonify
from flask_jwt_extended import decode_token

from app.utils.errors.EmailNotSentException import EmailNotSentException


def getConnectionParameters(datasource):
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for ds in data['datasources']:
            if ds["name"] == datasource:
                return {"user": ds["user"],
                        "password": ds["password"],
                        "host": ds["host"],
                        "port": ds["port"],
                        "db": ds["db"]}
        raise Exception("Connection not found")

def getCountries():
    countries = json.load(open("../config/countries.json"))
    return countries

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

def send_html_email(email, subject, html_content):
    try:
        sender_email = 'dimaio.albe@gmail.com'
        receiver_email = email

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        message.attach(MIMEText(html_content, 'html'))

        smtp_server = 'smtp.gmail.com'
        smtp_port = 587
        smtp_username = 'dimaio.albe@gmail.com'
        smtp_password = 'zhntipqqmkpuspne'

        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()

        server.login(smtp_username, smtp_password)
        server.sendmail(sender_email, receiver_email, message.as_string())
        server.quit()
    except Exception:
        raise EmailNotSentException()


def getVariables(datasource):
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for ds in data['variables']:
            if ds['name'] == datasource:
                return ds

def getEmails(datasource):
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        for ds in data['emails']:
            if ds['name'] == datasource:
                return ds

def generatePinCode(size=6, chars=string.digits):
    return ''.join(random.choice(chars) for x in range(size))


def generateUuid(size=8):
    return str(uuid.uuid4())[:size]


def hashString(password: str):
    return hashlib.md5(password.encode('UTF-8')).hexdigest()


def createSuccessResponse(param):
    return jsonify({
        "date": str(datetime.now()),
        "success": True,
        "param": param,
        "code": 200,
    })


def getClient():
    with open('../config/config.yaml', 'r') as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
        return {
            'client_id': data['client']['client_id'],
            'client_secret': data['client']['client_secret']
        }


def getFormattedDateTime():
    return datetime.now().__str__() \
        .replace("-", "") \
        .replace(" ", "") \
        .replace(":", "") \
        .replace(".", "")


def createErrorResponse(error):
    return jsonify({
        "date": str(datetime.now()),
        "success": False,
        "error": {
            "message": error.message,
            "path": error.__module__
        },
        "code": error.code,
    }), error.code

def getPlaceDetails(placeId):
    place = requests.get(f"https://nominatim.openstreetmap.org/details?place_id={placeId}&format=json&addressdetails=addressdetails").json()
    print(place)
    return {
        'place_id': placeId,
        'name': place['localname'],
        'country': place['address'][-1]['localname'],
        'country_code': place['country_code'].upper()
    }


def createJWTToken(data, expires_delta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, "super-secret", algorithm="HS256")
    return encoded_jwt


def isTokenValid(token):
    try:
        tokenPayload = decode_token(token)
        return True
    except Exception:
        return False


"""
:description: Decodifica un video in base64 e lo salva
:param videoPath: str
:return: None
"""


def saveFile(base64Data, filePath):
    try:
        decoded_data = base64.b64decode(base64Data)
        with open(filePath, 'wb') as file:
            file.write(decoded_data)
    except Exception as exc:
        ...


BASE_FE_URL = getVariables('local')['BASE_FE_URL']
BASE_URL = getVariables('local')['BASE_URL']