# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
from flask import jsonify
from lin.redprint import Redprint

from app.models.banner import Banner
from app.models.banner_status import BannerStatus

banner_api = Redprint('banner')

@banner_api.route('/home/status')
def get_home_banner_status():
    """获取首页轮播图的状态"""
    status = BannerStatus.get_status()
    return jsonify(dict(value=status))

@banner_api.route('/home')
def get_home_banners():
    """获取首页轮播图数据"""
    banners = Banner.query.filter_by(delete_time=None).order_by(Banner._create_time.desc()).all()
    return jsonify(banners)
