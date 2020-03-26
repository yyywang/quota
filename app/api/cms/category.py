# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from flask import jsonify, current_app
from lin import admin_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import json_paginate
from app.models.category import Category
from app.validators.forms import CreateCategoryForm, UpdateCategoryForm, PaginationForm

category_api = Redprint('category')


@category_api.route('', methods=['POST'])
@admin_required
def create_category():
    form = CreateCategoryForm().validate_for_api()
    Category.create(content=form.content.data, commit=True)
    return Success()

@category_api.route('/<int:cid>')
@admin_required
def get_category(cid):
    category = Category.query.filter_by(id=cid, delete_time=None).first_or_404()
    return jsonify(category)

@category_api.route('')
@admin_required
def get_categorys():
    """获取所有标签，分页返回"""
    categorys = Category.query.filter_by(delete_time=None).order_by(
        Category._create_time.desc()).all()

    return jsonify(categorys)

@category_api.route('/<int:cid>', methods=['PUT'])
@admin_required
def update_category(cid):
    form = UpdateCategoryForm().validate_for_api()
    Category.update_category(cid, form)
    return Success()

@category_api.route('/<int:cid>', methods=['DELETE'])
@admin_required
def delete_category(cid):
    Category.remove_category(cid)
    return Success()