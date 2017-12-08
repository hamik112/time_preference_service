from random import randint

import pytz
from flask import Flask, render_template, redirect, jsonify, current_app, request, session, g, abort, Blueprint,send_file

from constants import KEY_PREFIX_LAST_USER_NOTIFICATION_AT, USER_NOTIFICATION_TIME_RANGE
from dto.result import ResponseDto
from utils import flaskrun
import httplib2
import json
import urllib
import requests 
from extensions import redis, rq
import datetime
import base64
import io

application = Flask(__name__)
application.config.from_envvar('ADMIN_CONFIG_PATH',silent=True)

redis.init_app(application)
rq.init_app(application)



# Returns returns time preference for user
@application.route('/get_time_preference/', methods=["POST"])
def get_user_data():
    users = request.form.get("users")
    start_time = request.form.get("start-time")
    end_time = request.form.get("end-time")
    if users:
        users = users.split(',')
        user_time_preference_list = []
        response_dto = ResponseDto(result = user_time_preference_list)
        today_seven_pm_time = int(datetime.datetime.combine(datetime.date.today(),
                                                            datetime.time(13, 30)).strftime("%s"))
        for user in users:
            user_time_preference_list.append({'user_id': user,
                                              'suggested_time': today_seven_pm_time +
                                                                 randint(0, USER_NOTIFICATION_TIME_RANGE)})
        return response_dto.to_json()
    return ResponseDto(status=-1, msg='user list not present').to_json()


@application.route('/set_user_access/', methods=["POST"])
def set_user_last_notification_time():
    user = request.form.get("user")
    last_accessed_time = request.form.get("notification-time")
    if user and last_accessed_time and last_accessed_time.isdigit():
        key_for_last_notification_time = '{}{}'.format(KEY_PREFIX_LAST_USER_NOTIFICATION_AT, user)
        last_accessed_time_in_redis = redis.get(key_for_last_notification_time)
        if not last_accessed_time_in_redis or long(last_accessed_time_in_redis) < long(last_accessed_time):
            redis.set(key_for_last_notification_time, last_accessed_time)
        return ResponseDto(status=0, msg='success').to_json()
    return ResponseDto(status=-1, msg='args invalid').to_json()


if __name__ == "__main__":
    flaskrun(application, default_port=5003)

