"""
    :copyright: © 2019 by the Lin team.
    :license: MIT, see LICENSE for more details.
"""

from flask import Blueprint
from app.api.v1.client import client_api
from app.api.v1.user import user_api
from .quota import quota_api
from app.api.v1.banner import banner_api
from .category import category_api
from .ad import ad_api
from app.api.v1 import token


def create_v1():
    bp_v1 = Blueprint('v1', __name__)
    quota_api.register(bp_v1)
    banner_api.register(bp_v1)
    category_api.register(bp_v1)
    ad_api.register(bp_v1)
    user_api.register(bp_v1)
    client_api.register(bp_v1)
    token.api.register(bp_v1)

    return bp_v1
