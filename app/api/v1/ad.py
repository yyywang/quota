# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from flask import current_app, jsonify
from lin.redprint import Redprint
from sqlalchemy import func

from app.libs.utils import json_paginate
from app.models.ad import Ad
from app.models.category import Category
from app.validators.forms import GetAdsForm

ad_api = Redprint('ads')

@ad_api.route('')
def get_ads():
    form = GetAdsForm().validate_for_api()
    per_page = current_app.config['COUNT_DEFAULT']
    if form.category.data == '全部':
        ads = Ad.query.filter_by(delete_time=None).order_by(
            Ad._create_time.desc()).paginate(form.page.data, per_page)
    else:
        category = Category.query.filter_by(content=form.category.data).first_or_404()
        ads = Ad.query.with_parent(category).filter_by(delete_time=None).order_by(
            Ad._create_time.desc()).paginate(form.page.data, per_page)

    return jsonify(json_paginate(ads))

@ad_api.route('/random')
def get_random_ad():
    """随机返回一条广告数据"""
    ad = Ad.query.filter_by(delete_time=None).order_by(func.rand()).limit(1).all()
    return jsonify(ad)