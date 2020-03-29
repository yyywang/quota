# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from flask import current_app, jsonify
from flask_jwt_extended import get_current_user
from lin import login_required
from lin.redprint import Redprint

from app.libs.utils import paginate_data, rm_deleted_data, rm_paginate_deleted_data
from app.validators.forms import PaginationForm

user_api = Redprint('user')

@user_api.route('/collections')
@login_required
def get_collected_quotas():
    """获取我的收藏"""
    form = PaginationForm().validate_for_api()
    per_page = current_app.config['COUNT_DEFAULT']
    current_uer = get_current_user()
    paginate = paginate_data(current_uer.not_deleted_collected_quotas, form.page.data, per_page)
    return jsonify(paginate)

@user_api.route('/likes')
@login_required
def get_liked_quotas():
    """获取我的点赞"""
    form = PaginationForm().validate_for_api()
    per_page = current_app.config['COUNT_DEFAULT']
    current_uer = get_current_user()
    paginate = paginate_data(current_uer.not_deleted_liked_quotas, form.page.data, per_page)
    return jsonify(paginate)