from flask import Blueprint, session, g, send_file
from flask.json import jsonify
from flask.globals import request
from flask.templating import render_template
from werkzeug.utils import redirect
from datetime import datetime, timedelta
from collections import Counter
import time
import math
import hashlib
import os
from models import db, User
import binascii
import requests
from os.path import getsize
import sys

bp = Blueprint('', __name__, url_prefix='')

@bp.route("/bin", methods=["POST", "GET"])
def read_bin():
    rawData = request.get_json()
    # address = rawData["data"]

    print(f'Firmware File Size : {getsize("/home/eternelgyu/OTA/firmware/sketch_oct28a.ino.hex") / 1000}kb')
    print("Device Connected!")
    # print(f'Device Address : {address}')

    # with open('/home/eternelgyu/OTA/firmware/test_firmware.bin', 'rb') as f:
    with open('/home/eternelgyu/OTA/firmware/sketch_oct28a.ino.hex', 'rb') as f:

        content = f.readlines()
        hex_content = [f'{i[0:-2]}' for i in content]


    # with open('/home/eternelgyu/OTA/firmware/sketch_oct28a.ino.hex', 'rb') as f:

    #     content = f.readline()

    #     binaryDataString = ["{:02x}".format(x) for x in content]
    #     print(binaryDataString)

        # content_to_hex = binascii.hexlify(content)
        # test = []
        # test.append(content_to_hex)
        # content_to_string = str(content_to_hex)

        # unit = 100
        # slice_content = [content_to_string[i : i + unit] for i in range(0, len(content_to_string), unit)]
        # print(len(slice_content))

    return jsonify({
        "data" : hex_content
    })

    # return jsonify({
    #     "data" : content_to_string
    # })


@bp.route("/test")
def test():
    print(request.form["files"])

    return 0

@bp.route("/login")
def login_page():
    return render_template("login.html")

@bp.route("/user")
def user_page():
    return render_template("user.html")

@bp.route("/regi_check", methods=["POST"])
def register_chk():
    rawData = request.get_json()

    # print(rawData)

    userId = rawData["userId"]
    password = rawData["password"]
    email = rawData["email"]

    print(userId)
    print(password)
    print(email)

    chk_user = User.query.filter(User.user_id == userId).first()

    if chk_user and userId is not None:
        return jsonify({"msg" : "userId alrealy exist."})
    else:
        db.session.add(User(user_id = userId, email = email, password = password))
        db.session.commit()

    return "Done"

@bp.route("/login_check", methods=["POST", "GET"])
def login_chk():
    # rawData = request.get_json()

    # print(rawData)

    userId = request.args.get('userId')
    password = request.args.get('password')
    # email = rawData["email"]

    print(userId)
    print(password)
    # print(email)

    chk_user = User.query.filter(User.user_id == userId).filter(User.password == password).first()

    if chk_user:
        return render_template("main_view.html")
    else:
        return jsonify({"msg" : "wrong password"})



# @bp.route()

target_file_path = '/home/eternelgyu/OTA/firmware/test_firmware.bin'
company_name = "KETI"
build_num = 2
build_date = '20-10-2022'
API_KEY = 'test'

@bp.route('/update', methods=["POST"])
def api_update():
    if request.method == "POST":
        key = request.form['api_key']
        target_path = request.form['target_path']

        print(API_KEY == key)

        if API_KEY == key and len(target_path) > 1:
            try:
                return send_file(target_file_path)
            except Exception as e:
                return str(e)

def version():
    size = os.path.getsize(target_file_path)
    print(f'Size of file is {size} bytes')

    with open(target_file_path, "rb") as file_to_check:
        data = file_to_check.read()
        md5_returned = hashlib.md5(data).hexdigest()
        print(f'md5_checksum is {md5_returned}')

        value = {
            "companyName" : company_name,
            "buildNum" : build_num,
            "buildDate" : build_date,
            "serverFilePath" : target_file_path,
            "fileSize" : size,
            "md5Checksum" : md5_returned
        }

        return jsonify(value)


    # "firmwareName" : "base1.1"
    # "buildNum" : "1.1"
    # "buildDate" : "2022-10-24"
    # "serverFilePath" : ""
    # "fileSize" : "14.592kb"
    # "md5Checksum" : "m52kdosajn123l4m2"

    # "firmwareVer" : "1.0"
    # "selectVer" : "1.1"

    # "deviceAddr" : "E5:1B:E4:8A:9E:8A"
    # "datetime" : "2022-10-24 18:04:00"


@bp.route("/", methods = ["GET"])
def mainView():
    
    return render_template("main_view.html")

@bp.route("/get_version")
def api_version():
    return version()

@bp.route('/get_time')
def api_localtime():
    current_local = time.localtime()
    gmt_offset = current_local.tm_gmtoff
    local_timestamp = time.mktime(current_local)

    return jsonify({
        "timestamp" : local_timestamp
    })

