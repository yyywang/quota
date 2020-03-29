# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from flask import jsonify
from flask_jwt_extended import get_current_user
from lin import login_required
from lin.exception import ParameterException, Success
from lin.redprint import Redprint
from sqlalchemy import func
from app.libs.utils import json_paginate
from app.models.ad import Ad
from app.models.category import Category
from app.models.quota import Quota
from app.validators.forms import GetQuotasForm

quota_api = Redprint('quotas')

@quota_api.route('')
@login_required
def get_quotas():
    """
    获取短句，9个短句+1个广告
    :return: 
    """
    form = GetQuotasForm().validate_for_api()
    per_page = 9

    # 随机获取短句
    if form.order_by.data == 'random':
        if form.category.data != '全部':
            category = Category.query.filter_by(content=form.category.data).first_or_404()
            items = Quota.query.with_parent(category).filter_by(delete_time=None).order_by(func.rand()).limit(9).all()
        else:
            items = Quota.query.filter_by(delete_time=None).order_by(func.rand()).limit(9).all()
        # 将语录格式整理为分页格式
        quotas = {
            'items': items,
            'has_next': True,
            'page': form.page.data,
            'next_page': form.page.data + 1
        }
    # 按发布时间降序获取短句
    elif form.order_by.data == 'desc':
        if form.category.data != '全部':
            category = Category.query.filter_by(content=form.category.data).first_or_404()
            # 若有分类参数，则按类别查数据
            quotas = Quota.query.with_parent(category).filter_by(delete_time=None).order_by(
                Quota._create_time.desc()).paginate(form.page.data, per_page)
        else:
            quotas = Quota.query.filter_by(delete_time=None).order_by(
                Quota._create_time.desc()).paginate(form.page.data, per_page)
        quotas = json_paginate(quotas)
    else:
        raise ParameterException()

    ad = Ad.query.filter_by(delete_time=None).order_by(func.rand()).limit(1).first()
    if ad is not None:
        quotas['items'].append(ad)

    return jsonify(quotas)

@quota_api.route('/<int:qid>')
@login_required
def get_quota(qid):
    """返回 id=id 的具体数据"""
    quota = Quota.query.filter_by(id=qid, delete_time=None).first_or_404()
    return jsonify(quota)

@quota_api.route('/<int:qid>/like-or-not', methods=['PUT'])
@login_required
def like_or_not_quota(qid):
    """点赞/取消点赞语录"""
    current_user = get_current_user()
    quota = Quota.query.filter_by(delete_time=None, id=qid).first_or_404()
    is_like = current_user.like_or_not_quota(quota)
    return jsonify(dict(is_like=is_like))

@quota_api.route('/<int:qid>/collect-or-not', methods=['PUT'])
@login_required
def collect_or_not_quota(qid):
    """收藏/取消收藏语录"""
    current_user = get_current_user()
    quota = Quota.query.filter_by(delete_time=None, id=qid).first_or_404()
    is_collect = current_user.collect_or_not_quota(quota)
    return jsonify(dict(is_collect=is_collect))