# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from flask import current_app, jsonify
from lin import admin_required
from lin.exception import Success
from lin.redprint import Redprint
from app.libs.utils import json_paginate
from app.models.ad import Ad
from app.validators.forms import CreateAdForm, PaginationForm, UpdateAdForm, AdSetCategoryForm

ad_api = Redprint('ad')

@ad_api.route('', methods=['POST'])
@admin_required
def create_ad():
    """创建广告"""
    form = CreateAdForm().validate_for_api()
    Ad.create(
        des=form.des.data,
        cover_url=form.cover_url.data,
        link_url = form.link_url.data,
        category_id=form.category_id.data,
        commit=True
    )
    return Success()

@ad_api.route('')
@admin_required
def get_ads():
    form = PaginationForm().validate_for_api()
    per_page = current_app.config.get('COUNT_DEFAULT')

    paginate = Ad.query.filter_by(delete_time=None).order_by(
        Ad._create_time.desc()).paginate(form.page.data, per_page)

    return jsonify(json_paginate(paginate))

@ad_api.route('/<int:aid>')
@admin_required
def get_ad(aid):
    ad = Ad.query.filter_by(id=aid, delete_time=None).first_or_404()
    return jsonify(ad)

@ad_api.route('/<int:aid>', methods=['PUT'])
@admin_required
def update_ad(aid):
    form = UpdateAdForm().validate_for_api()
    Ad.update_ad(aid, form.data)
    return Success()

@ad_api.route('/<int:aid>', methods=['DELETE'])
@admin_required
def delete_ad(aid):
    Ad.remove_ad(aid)
    return Success()

@ad_api.route('/<int:aid>/category/set', methods=['POST'])
@admin_required
def set_categroy(aid):
    """为短句设置分类"""
    form = AdSetCategoryForm().validate_for_api()
    Ad.set_category(aid, form.category_id.data)
    return Success()