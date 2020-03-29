# -*- coding: utf-8 -*-
"""
  Created by Wesley on 2020/3/26.
"""
import uuid

from lin import db
from lin.core import User as _User, manager
from lin.exception import Forbidden, Success, AuthFailed
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from app.libs.wx import wx_get_user_by_code
from app.models.association_tables import like_and_quota, collect_and_quota


class CUser(_User):
    wx_open_id = Column(String(190)) # 微信 openid
    liked_quotas = relationship('Quota', secondary=like_and_quota, back_populates='liked_users') # 该用户点赞的语录
    collected_quotas = relationship('Quota', secondary=collect_and_quota, back_populates='collected_users')  # 该用户收藏的语录


    @staticmethod
    def verify_mina(account, secret):
        """
        校验小程序是否已注册
        :param account: 小程序 code
        :param secret: None
        :return: 
        """
        openid = wx_get_user_by_code(account)['openid']
        user = manager.user_model.query.filter_by(wx_open_id=openid, delete_time=None) \
            .first_or_404()
        if not user.is_active:
            raise AuthFailed(msg='您目前处于未激活状态，请联系超级管理员')
        return user

    @staticmethod
    def register_by_mina(wx_open_id):
        user = manager.user_model.query.filter_by(wx_open_id=wx_open_id).first()
        if user:
            raise Forbidden(msg='openid has been registered')
        else:
            with db.auto_commit():
                user = manager.user_model()
                user.wx_open_id = wx_open_id
                user.username = 'mina_' + str(manager.user_model.query.count())
                db.session.add(user)
            return Success()

    def like_or_not_quota(self, quota):
        """点赞/取消点赞语录"""
        with db.auto_commit():
            # 如果已点赞
            if quota in self.liked_quotas:
                self.liked_quotas.remove(quota)
                is_like = False
            # 未点赞
            else:
                self.liked_quotas.append(quota)
                is_like = True
        return is_like

    def collect_or_not_quota(self, quota):
        """收藏/取消收藏语录"""
        with db.auto_commit():
            # 如果已收藏
            if quota in self.collected_quotas:
                self.collected_quotas.remove(quota)
                is_collect = False
            # 未收藏
            else:
                self.collected_quotas.append(quota)
                is_collect = True
        return is_collect

    @property
    def not_deleted_collected_quotas(self):
        # 去除被删除的语录
        return [item for item in self.collected_quotas if item.delete_time is None]

    @property
    def not_deleted_liked_quotas(self):
        # 去除被删除的语录
        return [item for item in self.liked_quotas if item.delete_time is None]