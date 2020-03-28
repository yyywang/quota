# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/24.
"""
from lin import db
from lin.core import manager
from app.models.banner_status import BannerStatus


def init_admin():
    """初始化超级管理员"""
    admin = manager.user_model.query.filter_by(username='super', delete_time=None).first()
    if admin is None:
        with db.auto_commit():
            # 创建一个超级管理员
            user = manager.user_model()
            user.username = 'super'
            user.password = '123456'
            user.email = '1234995678@qq.com'
            # admin 2 的时候为超级管理员，普通用户为 1
            user.admin = 2
            db.session.add(user)

def init_banner_status():
    """初始化轮播图状态"""
    banner_status = BannerStatus.query.filter_by(delete_time=None).first()
    if banner_status is None:
        with db.auto_commit():
            banner_status = BannerStatus()
            db.session.add(banner_status)