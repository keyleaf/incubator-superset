# -*- coding: utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals

from flask import current_app

import requests

import logging

logger = logging.getLogger(__name__)


# print(current_app.config.get('REMOTE_SERVER_API'))
# url = "http://192.168.1.51:9003/api/login"
# # headers = {'Content-Type':'application/json;charset=UTF-8'}
# data = {"username":"admin","password":"123"}
# r = requests.post(url, json=data)
#
# print('success')
# print(r.json())


class AuthCenter(object):
    logger.info("using customize AuthCenter")

    @staticmethod
    def authenticate(username, password):
        data = {"username": username, "password": password}
        url = "http://192.168.1.26:9003/api/login"
        # url = "http://192.168.1.51:9003/api/login"
        r = requests.post(url, json=data)
        print(r.json()["success"])
        if r and r.json()["success"]:
            return data
        else:
            return None
