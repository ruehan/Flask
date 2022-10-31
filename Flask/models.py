from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql.sqltypes import BigInteger, Boolean
from sqlalchemy.dialects.mysql import DATETIME, BIGINT
from datetime import datetime, timedelta

db = SQLAlchemy()

from enum import unique

# ScaleInbody (scale_inbody)

class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

class Firmware(db.Model):
    __tablename__ = "firmware"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String)
    device_addr = db.Column(db.String)
    firmware_name = db.Column(db.String)
    firmware_ver = db.Column(db.Float)

class FirmwareList(db.Model):
    __tablename__ = "firmware_list"

    id = db.Column(db.Integer, primary_key=True)
    firmware_name = db.Column(db.String)
    firmware_ver = db.Column(db.Float)
    release_date = db.Column(db.String)