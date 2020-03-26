# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/23.
"""
from flask import current_app, jsonify
from lin import admin_required
from lin.exception import Success
from lin.redprint import Redprint
from app.libs.utils import json_paginate
from app.models.quota import Quota
from app.validators.forms import CreateQuotaForm, PaginationForm, QuotaSetCategoryForm

quota_api = Redprint('quota')

@quota_api.route('', methods=['POST'])
@admin_required
def create_quota():
    """创建语录"""
    form = CreateQuotaForm().validate_for_api()
    Quota.create(
        content=form.content.data,
        content_text=form.content.plain_text,
        category_id=form.category_id.data,
        commit=True)
    return Success()

@quota_api.route('', methods=['GET'])
@admin_required
def get_quotas():
    """获取语录，分页返回"""
    form = PaginationForm().validate_for_api()
    per_page = current_app.config.get('COUNT_DEFAULT')

    paginate = Quota.query.filter_by(delete_time=None).order_by(
        Quota._create_time.desc()).paginate(form.page.data, per_page)

    return jsonify(json_paginate(paginate))

@quota_api.route('/<int:qid>')
@admin_required
def get_quota(qid):
    """获取语录具体信息"""
    quota = Quota.query.filter_by(delete_time=None, id=qid).first_or_404()
    return jsonify(quota)

@quota_api.route('/<int:qid>', methods=['PUT'])
@admin_required
def update_quota(qid):
    """更新id=qid的语录信息"""
    form = CreateQuotaForm().validate_for_api()
    Quota.update_quota(qid, form)
    return Success(msg='更新语录成功')

@quota_api.route('/<int:qid>', methods=['DELETE'])
@admin_required
def delete_quota(qid):
    Quota.remove_quota(qid)
    return Success(msg='语录删除成功')

@quota_api.route('/<int:qid>/category/set', methods=['POST'])
@admin_required
def set_categroy(qid):
    """为短句设置分类"""
    form = QuotaSetCategoryForm().validate_for_api()
    Quota.set_category(qid, form.category_id.data)
    return Success()