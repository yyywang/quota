# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from flask import jsonify, current_app
from lin import admin_required
from lin.exception import Success
from lin.redprint import Redprint

from app.libs.utils import json_paginate
from app.models.banner import Banner
from app.models.banner_status import BannerStatus
from app.validators.forms import CreateBannerForm, UpdateBannerForm, PaginationForm

banner_api = Redprint('banner')

@banner_api.route('/status')
@admin_required
def get_status():
    """获取轮播图状态"""
    status = BannerStatus.get_status()
    return jsonify(dict(value=status))

@banner_api.route('/open', methods=['POST'])
@admin_required
def open_banner():
    """打开轮播图"""
    BannerStatus.open()
    return Success()

@banner_api.route('/close', methods=['POST'])
@admin_required
def close_banner():
    """关闭轮播图"""
    BannerStatus.close()
    return Success()

@banner_api.route('', methods=['POST'])
@admin_required
def create_banner():
    """创建一个轮播图"""
    form = CreateBannerForm().validate_for_api()
    Banner.create_banner(form.data)
    return Success()

@banner_api.route('/<int:bid>')
@admin_required
def get_banner(bid):
    banner = Banner.query.filter_by(id=bid, delete_time=None).first_or_404()
    return jsonify(banner)

@banner_api.route('/<int:bid>', methods=['PUT'])
@admin_required
def update_banner(bid):
    """更新id=bid轮播图的信息"""
    form = UpdateBannerForm().validate_for_api()
    Banner.update_banner(bid, form.data)
    return Success()

@banner_api.route('/<int:bid>', methods=['DELETE'])
@admin_required
def delete_banner(bid):
    """删除id=bid的轮播图"""
    Banner.remove_banner(bid)
    return Success()

@banner_api.route('')
@admin_required
def get_banners():
    form = PaginationForm().validate_for_api()
    per_page = current_app.config.get('COUNT_DEFAULT')

    banners = Banner.query.filter_by(delete_time=None).order_by(
        Banner._create_time.desc()).paginate(form.page.data, per_page)

    return jsonify(json_paginate(banners))